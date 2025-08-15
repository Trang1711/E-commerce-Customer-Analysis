# src/reco_surprise.py
import pandas as pd
from surprise import Dataset, Reader, SVD, KNNBaseline
from sqlalchemy import text
from db import get_engine

def build_interactions():
    eng = get_engine()
    q = """
    SELECT o.customer_id AS user_id, oi.product_id AS item_id,
           SUM(oi.quantity) AS qty,
           SUM(oi.quantity * oi.unit_price) AS revenue
    FROM dbo.orders o
    JOIN dbo.order_items oi ON o.order_id = oi.order_id
    GROUP BY o.customer_id, oi.product_id
    HAVING SUM(oi.quantity) > 0
    """
    df = pd.read_sql_query(text(q), eng)
    df["rating"] = (1 + (df["revenue"]).apply(lambda x: np.log1p(x))).clip(upper=5.0)
    return df[["user_id","item_id","rating"]]

def train_surprise(model_type="SVD"):
    df = build_interactions()
    reader = Reader(rating_scale=(1,5))
    data = Dataset.load_from_df(df[["user_id","item_id","rating"]], reader)
    trainset = data.build_full_trainset()

    if model_type == "SVD":
        algo = SVD(n_factors=50, reg_all=0.02, n_epochs=30, random_state=42)
    else:
        algo = KNNBaseline(sim_options={"name":"pearson_baseline","user_based":True})

    algo.fit(trainset)
    return algo, trainset

def recommend_topn(algo, trainset, user_id, n=10):
    # items chưa mua
    inner_uid = trainset.to_inner_uid(str(user_id))
    purchased = set([iid for (iid, _) in trainset.ur[inner_uid]])
    all_items = set(range(trainset.n_items))
    candidates = list(all_items - purchased)
    preds = []
    for inner_iid in candidates:
        pred = algo.predict(uid=str(user_id), iid=trainset.to_raw_iid(inner_iid))
        preds.append((pred.iid, pred.est))
    preds.sort(key=lambda x: x[1], reverse=True)
    return preds[:n]

def bulk_generate_and_persist_topn(n=10):
    algo, trainset = train_surprise("SVD")
    eng = get_engine()
    users = [trainset.to_raw_uid(u) for u in range(trainset.n_users)]
    rows = []
    for uid in users:
        recs = recommend_topn(algo, trainset, uid, n=n)
        for rank, (pid, score) in enumerate(recs, start=1):
            rows.append((uid, pid, rank, float(score)))
    df = pd.DataFrame(rows, columns=["customer_id","product_id","rank_order","score"])
    with eng.begin() as conn:
        conn.execute(text("TRUNCATE TABLE dbo.recommendations"))
        df.to_sql("recommendations", conn, if_exists="append", index=False)
