# src/api.py
from flask import Flask, jsonify, request
from sqlalchemy import text
from db import get_engine
from config import API_TOKEN

app = Flask(__name__)
eng = get_engine()

def auth_ok(req):
    return req.headers.get("X-API-KEY") == API_TOKEN

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/segments/<customer_id>")
def get_segment(customer_id):
    q = text("""
        SELECT customer_id, recency_days, frequency, monetary, r_score, f_score, m_score, segment_label
        FROM dbo.customer_rfm WHERE customer_id = :cid
    """)
    with eng.begin() as conn:
        row = conn.execute(q, {"cid": str(customer_id)}).mappings().first()
    if not row:
        return jsonify({"error":"customer not found"}), 404
    return jsonify(dict(row))

@app.get("/recommendations/<customer_id>")
def get_reco(customer_id):
    k = int(request.args.get("k", 10))
    q = text("""
      SELECT r.customer_id, r.product_id, r.rank_order, r.score, p.description, p.unit_price
      FROM dbo.recommendations r
      LEFT JOIN dbo.products p ON r.product_id = p.product_id
      WHERE r.customer_id = :cid
      ORDER BY r.rank_order
    """)
    with eng.begin() as conn:
        rows = conn.execute(q, {"cid": str(customer_id)}).mappings().all()
    return jsonify({"customer_id": customer_id, "topN": rows[:k]})
