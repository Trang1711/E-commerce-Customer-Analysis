# src/etl.py
import pandas as pd
from sqlalchemy import text
from db import get_engine

def load_transactions(csv_path="data/transactions.csv"):
    df = pd.read_csv(csv_path)  # or read_parquet
    # Chuẩn hoá tối thiểu:
    df = df.rename(columns={
        "InvoiceNo":"order_id",
        "InvoiceDate":"order_datetime",
        "CustomerID":"customer_id",
        "StockCode":"product_id",
        "Description":"description",
        "Quantity":"quantity",
        "UnitPrice":"unit_price"
    })

    df["order_datetime"] = pd.to_datetime(df["order_datetime"])
    df["revenue"] = df["quantity"] * df["unit_price"]

    # Tách bảng dimension + fact
    customers = (df[["customer_id"]]
                 .dropna().drop_duplicates()
                 .astype({"customer_id":str}))
    products = (df[["product_id","description","unit_price"]]
                .drop_duplicates()
                .astype({"product_id":str}))
    orders = (df[["order_id","order_datetime","customer_id"]]
              .drop_duplicates()
              .astype({"order_id":str,"customer_id":str}))
    items  = (df[["order_id","product_id","quantity","unit_price"]]
              .astype({"order_id":str,"product_id":str,"quantity":int}))

    eng = get_engine()
    with eng.begin() as conn:
        customers.to_sql("customers", conn, if_exists="append", index=False)
        products.to_sql("products", conn, if_exists="append", index=False)
        orders.to_sql("orders", conn, if_exists="append", index=False)
        items.to_sql("order_items", conn, if_exists="append", index=False)
        # Cập nhật first/last purchase
        conn.execute(text("""
            UPDATE c SET
              c.first_purchase = x.first_purchase,
              c.last_purchase  = x.last_purchase
            FROM dbo.customers c
            JOIN (
              SELECT customer_id,
                     MIN(order_datetime) AS first_purchase,
                     MAX(order_datetime) AS last_purchase
              FROM dbo.orders
              GROUP BY customer_id
            ) x ON c.customer_id = x.customer_id
        """))
