# main.py - File chính để chạy dự án ecommerce
from src.api import app
from src.config import API_TOKEN

if __name__ == "__main__":
    print(f"🚀 Khởi động Ecommerce API...")
    print(f"🔑 API Token: {API_TOKEN}")
    print(f"📊 Health check: http://localhost:5000/health")
    print(f"👥 Segments: http://localhost:5000/segments/<customer_id>")
    print(f"🎯 Recommendations: http://localhost:5000/recommendations/<customer_id>")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
