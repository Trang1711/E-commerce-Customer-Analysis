# demo_api.py - Demo API đơn giản cho dự án ecommerce
from flask import Flask, jsonify, request, render_template_string
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import json

app = Flask(__name__)

# Demo data - thay thế cho database
demo_customers = {
    "C001": {"recency_days": 5, "frequency": 15, "monetary": 2500, "segment": "VIP"},
    "C002": {"recency_days": 30, "frequency": 8, "monetary": 1200, "segment": "Regular"},
    "C003": {"recency_days": 90, "frequency": 3, "monetary": 500, "segment": "At Risk"},
    "C004": {"recency_days": 15, "frequency": 12, "monetary": 1800, "segment": "Regular"},
    "C005": {"recency_days": 2, "frequency": 25, "monetary": 3500, "segment": "VIP"}
}

demo_products = [
    {"product_id": "P001", "name": "Laptop Gaming", "price": 1500, "category": "Electronics"},
    {"product_id": "P002", "name": "Smartphone", "price": 800, "category": "Electronics"},
    {"product_id": "P003", "name": "Headphones", "price": 200, "category": "Electronics"},
    {"product_id": "P004", "name": "T-shirt", "price": 25, "category": "Clothing"},
    {"product_id": "P005", "name": "Jeans", "price": 80, "category": "Clothing"},
    {"product_id": "P006", "name": "Shoes", "price": 120, "category": "Clothing"},
    {"product_id": "P007", "name": "Book", "price": 15, "category": "Books"},
    {"product_id": "P008", "name": "Coffee Maker", "price": 150, "category": "Home"},
    {"product_id": "P009", "name": "Blender", "price": 100, "category": "Home"},
    {"product_id": "P010", "name": "Watch", "price": 300, "category": "Accessories"}
]

# Demo recommendations
demo_recommendations = {
    "C001": ["P001", "P002", "P003", "P008", "P010"],
    "C002": ["P004", "P005", "P006", "P007", "P009"],
    "C003": ["P007", "P004", "P005", "P009", "P008"],
    "C004": ["P002", "P003", "P010", "P001", "P008"],
    "C005": ["P001", "P002", "P003", "P010", "P008"]
}

# HTML Template với màu xanh pastel
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Ecommerce Analytics</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #B0E2FF 0%, #87CEEB 100%);
            min-height: 100vh;
            color: #2c3e50;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(176, 226, 255, 0.3);
            text-align: center;
            border: 2px solid #B0E2FF;
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 15px;
            font-weight: 300;
        }
        
        .header p {
            color: #5a6c7d;
            font-size: 1.2em;
            font-weight: 400;
        }
        
        .nav {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(176, 226, 255, 0.2);
            border: 1px solid #B0E2FF;
        }
        
        .nav a {
            display: inline-block;
            padding: 12px 24px;
            margin: 8px;
            background: linear-gradient(45deg, #B0E2FF, #87CEEB);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            transition: all 0.3s ease;
            font-weight: 500;
            box-shadow: 0 2px 10px rgba(176, 226, 255, 0.3);
        }
        
        .nav a:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(176, 226, 255, 0.5);
            background: linear-gradient(45deg, #87CEEB, #B0E2FF);
        }
        
        .content {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(176, 226, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid #B0E2FF;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 4px 20px rgba(176, 226, 255, 0.15);
            border-left: 4px solid #B0E2FF;
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(176, 226, 255, 0.25);
        }
        
        .card h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.4em;
            font-weight: 600;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 25px;
            margin: 25px 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #B0E2FF, #87CEEB);
            color: white;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(176, 226, 255, 0.3);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(176, 226, 255, 0.4);
        }
        
        .stat-card h4 {
            font-size: 2.2em;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .stat-card p {
            opacity: 0.95;
            font-size: 1.1em;
            font-weight: 500;
        }
        
        .customer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
            margin: 25px 0;
        }
        
        .customer-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(176, 226, 255, 0.15);
            border-top: 4px solid #B0E2FF;
            transition: transform 0.3s ease;
        }
        
        .customer-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 6px 25px rgba(176, 226, 255, 0.25);
        }
        
        .customer-card h3 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.3em;
        }
        
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin: 25px 0;
        }
        
        .product-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 20px rgba(176, 226, 255, 0.15);
            text-align: center;
            transition: transform 0.3s ease;
            border: 1px solid #f0f8ff;
        }
        
        .product-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(176, 226, 255, 0.3);
        }
        
        .product-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .price {
            font-size: 1.6em;
            color: #B0E2FF;
            font-weight: bold;
            margin: 15px 0;
        }
        
        .category {
            background: #f0f8ff;
            color: #5a6c7d;
            padding: 8px 18px;
            border-radius: 20px;
            font-size: 0.9em;
            display: inline-block;
            border: 1px solid #B0E2FF;
        }
        
        .segment-badge {
            padding: 8px 18px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            display: inline-block;
            margin: 10px 0;
        }
        
        .segment-vip { 
            background: #e74c3c; 
            box-shadow: 0 2px 10px rgba(231, 76, 60, 0.3);
        }
        .segment-regular { 
            background: #3498db; 
            box-shadow: 0 2px 10px rgba(52, 152, 219, 0.3);
        }
        .segment-at-risk { 
            background: #f39c12; 
            box-shadow: 0 2px 10px rgba(243, 156, 18, 0.3);
        }
        
        .btn {
            background: linear-gradient(45deg, #B0E2FF, #87CEEB);
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
            box-shadow: 0 2px 10px rgba(176, 226, 255, 0.3);
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(176, 226, 255, 0.5);
            background: linear-gradient(45deg, #87CEEB, #B0E2FF);
        }
        
        .footer {
            text-align: center;
            margin-top: 50px;
            color: rgba(44, 62, 80, 0.7);
            font-size: 0.9em;
        }
        
        .info-list {
            list-style: none;
            margin: 20px 0;
        }
        
        .info-list li {
            padding: 8px 0;
            border-bottom: 1px solid #f0f8ff;
            color: #5a6c7d;
        }
        
        .info-list li:last-child {
            border-bottom: none;
        }
        
        .info-list strong {
            color: #2c3e50;
            margin-right: 10px;
        }
        
        .back-buttons {
            margin-top: 30px;
            text-align: center;
        }
        
        .rank-badge {
            background: #B0E2FF;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            margin-bottom: 20px;
            font-weight: bold;
            font-size: 1.1em;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Ecommerce Analytics & Recommendation System</h1>
            <p>Hệ thống phân tích khách hàng và gợi ý sản phẩm thông minh</p>
        </div>
        
        <div class="nav">
            <a href="/">Trang chủ</a>
            <a href="/customers">Khách hàng</a>
            <a href="/products">Sản phẩm</a>
            <a href="/analytics/summary">Thống kê</a>
            <a href="/segments/C001">Segments</a>
            <a href="/recommendations/C001">Gợi ý</a>
        </div>
        
        <div class="content">
            {{ content | safe }}
        </div>
        
        <div class="footer">
            <p>© 2025 Ecommerce Analytics System - Powered by Flask & Python</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <h2>Chào mừng đến với Ecommerce Analytics!</h2>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h4>5</h4>
            <p>Khách hàng</p>
        </div>
        <div class="stat-card">
            <h4>10</h4>
            <p>Sản phẩm</p>
        </div>
        <div class="stat-card">
            <h4>4</h4>
            <p>Segments</p>
        </div>
        <div class="stat-card">
            <h4>100%</h4>
            <p>Hiệu suất</p>
        </div>
    </div>
    
    <div class="card">
        <h3>Tính năng chính</h3>
        <ul class="info-list">
            <li><strong>RFM Analysis:</strong> Phân tích Recency, Frequency, Monetary</li>
            <li><strong>Customer Segmentation:</strong> Phân nhóm khách hàng bằng K-means</li>
            <li><strong>Recommendation System:</strong> Hệ thống gợi ý sản phẩm thông minh</li>
            <li><strong>Analytics Dashboard:</strong> Bảng điều khiển phân tích dữ liệu</li>
        </ul>
    </div>
    
    <div class="card">
        <h3>Cách sử dụng</h3>
        <p>Chọn một trong các menu phía trên để khám phá:</p>
        <ul class="info-list">
            <li><strong>Khách hàng:</strong> Xem danh sách và thông tin chi tiết</li>
            <li><strong>Sản phẩm:</strong> Khám phá catalog sản phẩm</li>
            <li><strong>Thống kê:</strong> Xem tổng quan dữ liệu</li>
            <li><strong>Segments:</strong> Phân tích nhóm khách hàng</li>
            <li><strong>Gợi ý:</strong> Xem sản phẩm được đề xuất</li>
        </ul>
    </div>
    """
    
    return render_template_string(HTML_TEMPLATE, title="Trang chủ", content=content)

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "message": "API đang hoạt động bình thường",
        "timestamp": pd.Timestamp.now().isoformat()
    })

@app.route('/customers')
def get_customers():
    content = f"""
    <h2>Danh sách khách hàng</h2>
    <p>Tổng cộng: <strong>{len(demo_customers)}</strong> khách hàng</p>
    
    <div class="customer-grid">
    """
    
    for customer_id, customer in demo_customers.items():
        segment_class = f"segment-{customer['segment'].lower().replace(' ', '-')}"
        content += f"""
        <div class="customer-card">
            <h3>Khách hàng {customer_id}</h3>
            <div>
                <span class="segment-badge {segment_class}">{customer['segment']}</span>
            </div>
            <ul class="info-list">
                <li><strong>Recency:</strong> {customer['recency_days']} ngày</li>
                <li><strong>Frequency:</strong> {customer['frequency']} lần mua</li>
                <li><strong>Monetary:</strong> ${customer['monetary']:,.0f}</li>
            </ul>
            <div style="margin-top: 20px; text-align: center;">
                <a href="/segments/{customer_id}" class="btn">Xem chi tiết</a>
            </div>
        </div>
        """
    
    content += "</div>"
    
    return render_template_string(HTML_TEMPLATE, title="Khách hàng", content=content)

@app.route('/products')
def get_products():
    content = f"""
    <h2>Danh sách sản phẩm</h2>
    <p>Tổng cộng: <strong>{len(demo_products)}</strong> sản phẩm</p>
    
    <div class="product-grid">
    """
    
    for product in demo_products:
        content += f"""
        <div class="product-card">
            <h3>{product['name']}</h3>
            <div class="price">${product['price']:,.0f}</div>
            <span class="category">{product['category']}</span>
            <p style="margin-top: 15px; color: #7f8c8d;">ID: {product['product_id']}</p>
        </div>
        """
    
    content += "</div>"
    
    return render_template_string(HTML_TEMPLATE, title="Sản phẩm", content=content)

@app.route('/segments/<customer_id>')
def get_segment(customer_id):
    if customer_id not in demo_customers:
        return jsonify({"error": "Không tìm thấy khách hàng"}), 404
    
    customer = demo_customers[customer_id]
    r_score = _calculate_r_score(customer["recency_days"])
    f_score = _calculate_f_score(customer["frequency"])
    m_score = _calculate_m_score(customer["monetary"])
    
    segment_class = f"segment-{customer['segment'].lower().replace(' ', '-')}"
    
    content = f"""
    <h2>Phân tích khách hàng {customer_id}</h2>
    
    <div class="card">
        <h3>Thông tin cơ bản</h3>
        <div style="margin: 20px 0;">
            <span class="segment-badge {segment_class}">{customer['segment']}</span>
        </div>
        <ul class="info-list">
            <li><strong>Recency:</strong> {customer['recency_days']} ngày</li>
            <li><strong>Frequency:</strong> {customer['frequency']} lần mua</li>
            <li><strong>Monetary:</strong> ${customer['monetary']:,.0f}</li>
        </ul>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h4>{r_score}</h4>
            <p>R Score</p>
        </div>
        <div class="stat-card">
            <h4>{f_score}</h4>
            <p>F Score</p>
        </div>
        <div class="stat-card">
            <h4>{m_score}</h4>
            <p>M Score</p>
        </div>
        <div class="stat-card">
            <h4>{r_score + f_score + m_score}</h4>
            <p>Tổng Score</p>
        </div>
    </div>
    
    <div class="card">
        <h3>Gợi ý sản phẩm</h3>
        <p>Xem gợi ý sản phẩm cho khách hàng này:</p>
        <div style="text-align: center; margin-top: 20px;">
            <a href="/recommendations/{customer_id}" class="btn">Xem gợi ý</a>
        </div>
    </div>
    
    <div class="back-buttons">
        <a href="/customers" class="btn">Quay lại danh sách</a>
    </div>
    """
    
    return render_template_string(HTML_TEMPLATE, title=f"Segment {customer_id}", content=content)

@app.route('/recommendations/<customer_id>')
def get_recommendations(customer_id):
    if customer_id not in demo_recommendations:
        return jsonify({"error": "Không tìm thấy khách hàng"}), 404
    
    k = int(request.args.get("k", 5))
    recommended_products = demo_recommendations[customer_id][:k]
    
    content = f"""
    <h2>Gợi ý sản phẩm cho khách hàng {customer_id}</h2>
    <p>Tổng cộng: <strong>{len(recommended_products)}</strong> sản phẩm được gợi ý</p>
    
    <div class="product-grid">
    """
    
    for i, product_id in enumerate(recommended_products):
        product = next((p for p in demo_products if p["product_id"] == product_id), None)
        if product:
            score = round(1.0 - (i * 0.1), 2)
            content += f"""
            <div class="product-card">
                <div class="rank-badge">#{i + 1}</div>
                <h3>{product['name']}</h3>
                <div class="price">${product['price']:,.0f}</div>
                <span class="category">{product['category']}</span>
                <p style="margin-top: 15px; color: #B0E2FF; font-weight: bold;">Score: {score}</p>
            </div>
            """
    
    content += "</div>"
    
    content += f"""
    <div class="back-buttons">
        <a href="/segments/{customer_id}" class="btn">Quay lại segment</a>
        <a href="/customers" class="btn">Danh sách khách hàng</a>
    </div>
    """
    
    return render_template_string(HTML_TEMPLATE, title=f"Gợi ý {customer_id}", content=content)

@app.route('/analytics/summary')
def get_analytics_summary():
    recency_values = [c["recency_days"] for c in demo_customers.values()]
    frequency_values = [c["frequency"] for c in demo_customers.values()]
    monetary_values = [c["monetary"] for c in demo_customers.values()]
    
    segment_counts = {}
    for customer in demo_customers.values():
        segment = customer["segment"]
        segment_counts[segment] = segment_counts.get(segment, 0) + 1
    
    content = f"""
    <h2>Tổng quan dữ liệu</h2>
    
    <div class="stats-grid">
        <div class="stat-card">
            <h4>{len(demo_customers)}</h4>
            <p>Tổng khách hàng</p>
        </div>
        <div class="stat-card">
            <h4>{len(demo_products)}</h4>
            <p>Tổng sản phẩm</p>
        </div>
        <div class="stat-card">
            <h4>${sum(monetary_values):,.0f}</h4>
            <p>Tổng doanh thu</p>
        </div>
        <div class="stat-card">
            <h4>{len(segment_counts)}</h4>
            <p>Số segments</p>
        </div>
    </div>
    
    <div class="card">
        <h3>Phân bố segments</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px;">
    """
    
    for segment, count in segment_counts.items():
        content += f"""
            <div style="background: #f8fbfe; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #B0E2FF;">
                <h4 style="color: #B0E2FF; margin-bottom: 10px;">{segment}</h4>
                <p style="font-size: 1.6em; font-weight: bold; color: #2c3e50;">{count}</p>
            </div>
        """
    
    content += """
        </div>
    </div>
    
    <div class="card">
        <h3>Thống kê RFM</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 25px; margin-top: 20px;">
    """
    
    content += f"""
            <div style="background: #f8fbfe; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #B0E2FF;">
                <h4 style="color: #B0E2FF; margin-bottom: 10px;">Recency (ngày)</h4>
                <p style="font-size: 1.6em; font-weight: bold; color: #2c3e50;">{min(recency_values)} - {max(recency_values)}</p>
                <p style="color: #7f8c8d; margin-top: 10px;">Trung bình: {np.mean(recency_values):.1f}</p>
            </div>
            
            <div style="background: #f8fbfe; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #B0E2FF;">
                <h4 style="color: #B0E2FF; margin-bottom: 10px;">Frequency (lần)</h4>
                <p style="font-size: 1.6em; font-weight: bold; color: #2c3e50;">{min(frequency_values)} - {max(frequency_values)}</p>
                <p style="color: #7f8c8d; margin-top: 10px;">Trung bình: {np.mean(frequency_values):.1f}</p>
            </div>
            
            <div style="background: #f8fbfe; padding: 20px; border-radius: 12px; text-align: center; border: 1px solid #B0E2FF;">
                <h4 style="color: #B0E2FF; margin-bottom: 10px;">Monetary ($)</h4>
                <p style="font-size: 1.6em; font-weight: bold; color: #2c3e50;">${min(monetary_values):,.0f} - ${max(monetary_values):,.0f}</p>
                <p style="color: #7f8c8d; margin-top: 10px;">Trung bình: ${np.mean(monetary_values):,.0f}</p>
            </div>
        </div>
    </div>
    """
    
    return render_template_string(HTML_TEMPLATE, title="Thống kê", content=content)

def _calculate_r_score(recency_days):
    """Tính R score dựa trên recency"""
    if recency_days <= 7:
        return 5
    elif recency_days <= 30:
        return 4
    elif recency_days <= 60:
        return 3
    elif recency_days <= 90:
        return 2
    else:
        return 1

def _calculate_f_score(frequency):
    """Tính F score dựa trên frequency"""
    if frequency >= 20:
        return 5
    elif frequency >= 15:
        return 4
    elif frequency >= 10:
        return 3
    elif frequency >= 5:
        return 2
    else:
        return 1

def _calculate_m_score(monetary):
    """Tính M score dựa trên monetary"""
    if monetary >= 3000:
        return 5
    elif monetary >= 2000:
        return 4
    elif monetary >= 1000:
        return 3
    elif monetary >= 500:
        return 2
    else:
        return 1

if __name__ == "__main__":
    print("Khởi động Ecommerce Demo API...")
    print("Health check: http://localhost:5000/health")
    print("Homepage: http://localhost:5000/")
    print("Customers: http://localhost:5000/customers")
    print("Products: http://localhost:5000/products")
    print("Analytics: http://localhost:5000/analytics/summary")
    print("Segments: http://localhost:5000/segments/C001")
    print("Recommendations: http://localhost:5000/recommendations/C001")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
