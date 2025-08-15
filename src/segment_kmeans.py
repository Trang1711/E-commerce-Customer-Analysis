# src/segment_kmeans.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from db import get_engine
from features_rfm import compute_rfm

SEGMENT_MAP = {
    0: "Champions",
    1: "Loyal",
    2: "Potential",
    3: "At Risk",
    4: "Hibernating"
}

def train_kmeans(k=4, random_state=42):
    rfm = compute_rfm()
    # Biến đổi
    r = np.log1p(rfm["recency_days"])
    f = np.log1p(rfm["frequency"])
    m = np.log1p(rfm["monetary"])
    X = pd.DataFrame({"R": r, "F": f, "M": m})
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    # (tuỳ chọn) chọn k bằng Elbow/Silhouette
    # sils = {k: silhouette_score(Xs, KMeans(k, n_init="auto", random_state=42).fit_predict(Xs)) for k in range(3,8)}

    kmeans = KMeans(n_clusters=k, n_init="auto", random_state=random_state)
    labels = kmeans.fit_predict(Xs)

    rfm["segment_label"] = [SEGMENT_MAP.get(lbl, f"Cluster {lbl}") for lbl in labels]

    eng = get_engine()
    with eng.begin() as conn:
        # Ghi/Upsert vào customer_rfm (đơn giản: xoá ghi lại)
        conn.execute(text("TRUNCATE TABLE dbo.customer_rfm"))
        payload = rfm[["customer_id","recency_days","frequency","monetary","segment_label"]].copy()
        payload["r_score"] = pd.qcut(-rfm["recency_days"], 5, labels=False, duplicates='drop') + 1  # recency nhỏ tốt → đảo dấu
        payload["f_score"] = pd.qcut(rfm["frequency"], 5, labels=False, duplicates='drop') + 1
        payload["m_score"] = pd.qcut(rfm["monetary"], 5, labels=False, duplicates='drop') + 1
        payload.to_sql("customer_rfm", conn, if_exists="append", index=False)

    return rfm
