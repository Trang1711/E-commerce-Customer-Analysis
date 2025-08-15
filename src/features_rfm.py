# src/features_rfm.py
import pandas as pd
from sqlalchemy import text
from db import get_engine

def compute_rfm(ref_date=None):
    eng = get_engine()
    ref_date_sql = "GETDATE()" if ref_date is None else f"'{pd.to_datetime(ref_date).strftime('%Y-%m-%d')}'"
    query = f"""
    WITH agg AS (
      SELECT
        o.customer_id,
        DATEDIFF(day, MAX(o.order_datetime), {ref_date_sql}) AS recency_days,
        COUNT(DISTINCT o.order_id) AS frequency,
        SUM(oi.quantity * oi.unit_price) AS monetary
      FROM dbo.orders o
      JOIN dbo.order_items oi ON o.order_id = oi.order_id
      GROUP BY o.customer_id
    )
    SELECT * FROM agg
    """
    rfm = pd.read_sql_query(text(query), eng)
    return rfm
