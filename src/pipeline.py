# src/pipeline.py
from etl import load_transactions
from segment_kmeans import train_kmeans
from reco_surprise import bulk_generate_and_persist_topn

def run_all():
    # 1) ETL (chạy 1 lần hoặc định kỳ khi có data mới)
    # load_transactions("data/transactions.csv")
    # 2) RFM + Segment
    train_kmeans(k=5)
    # 3) Reco Top-N
    bulk_generate_and_persist_topn(n=10)

if __name__ == "__main__":
    run_all()
