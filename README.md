# 🛒 Ecommerce Analytics & Recommendation System

Dự án này cung cấp một hệ thống phân tích khách hàng và gợi ý sản phẩm cho ecommerce, bao gồm:

## 🚀 Tính năng chính

- **RFM Analysis**: Phân tích Recency, Frequency, Monetary
- **Customer Segmentation**: Phân nhóm khách hàng sử dụng K-means clustering
- **Recommendation System**: Hệ thống gợi ý sản phẩm
- **REST API**: API để truy vấn thông tin segments và recommendations
- **ETL Pipeline**: Xử lý dữ liệu giao dịch
- **Demo Mode**: Chế độ demo với dữ liệu mẫu để test nhanh

## 📁 Cấu trúc dự án

```
ecommerce/
├── data/
│   └── data.csv              # Dữ liệu giao dịch
├── src/
│   ├── api.py                # Flask API endpoints
│   ├── config.py             # Cấu hình dự án
│   ├── db.py                 # Kết nối database
│   ├── etl.py                # ETL pipeline
│   ├── features_rfm.py       # Tính toán RFM features
│   ├── pipeline.py           # Pipeline chính
│   ├── reco_surprise.py      # Recommendation system
│   └── segment_kmeans.py     # Customer segmentation
├── demo_api.py               # Demo API với dữ liệu mẫu
├── demo_data_processor.py    # Xử lý dữ liệu demo
├── main.py                   # File chính để chạy API
├── requirements.txt           # Python dependencies
└── README.md                 # Hướng dẫn này
```

## 🛠️ Cài đặt

### 1. Cài đặt Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Cài đặt SQL Server ODBC Driver
- Windows: Tải từ Microsoft
- Linux: `sudo apt-get install unixodbc-dev`

### 3. Cấu hình database
Chỉnh sửa `src/config.py` với thông tin database của bạn:
```python
MSSQL_SERVER = "your_server"
MSSQL_DATABASE = "your_database"
MSSQL_USERNAME = "your_username"
MSSQL_PASSWORD = "your_password"
```

## 🚀 Chạy dự án

### Chạy Demo API (Khuyến nghị)
```bash
python demo_api.py
```

Demo API sẽ chạy tại: http://localhost:5000

### Chạy Data Processor
```bash
python demo_data_processor.py
```

### Chạy API gốc (cần database)
```bash
python main.py
```

### Chạy ETL Pipeline
```bash
python src/pipeline.py
```

## 📊 API Endpoints

### Demo API (demo_api.py)

#### Homepage
```
GET /
```

#### Health Check
```
GET /health
```

#### Customers
```
GET /customers
```

#### Products
```
GET /products
```

#### Customer Segments
```
GET /segments/{customer_id}
```

#### Product Recommendations
```
GET /recommendations/{customer_id}?k=5
```

#### Analytics Summary
```
GET /analytics/summary
```

### Production API (main.py)

#### Health Check
```
GET /health
```

#### Customer Segments
```
GET /segments/{customer_id}
Headers: X-API-KEY: secret123
```

#### Product Recommendations
```
GET /recommendations/{customer_id}?k=10
Headers: X-API-KEY: secret123
```

## 🔑 Authentication

Sử dụng header `X-API-KEY: secret123` cho các endpoints cần xác thực.

## 📈 Workflow

1. **Data Loading**: Load dữ liệu giao dịch từ CSV
2. **RFM Calculation**: Tính toán RFM scores
3. **Segmentation**: Phân nhóm khách hàng bằng K-means
4. **Recommendation**: Tạo gợi ý sản phẩm
5. **API Service**: Cung cấp dữ liệu qua REST API

## 🐛 Troubleshooting

- **Database Connection**: Kiểm tra thông tin kết nối trong `config.py`
- **ODBC Driver**: Đảm bảo đã cài đặt SQL Server ODBC Driver
- **Dependencies**: Chạy `pip install -r requirements.txt`

## 📝 Ghi chú

- **Demo Mode**: Sử dụng `demo_api.py` để chạy nhanh mà không cần database
- **Production Mode**: Sử dụng `main.py` với SQL Server database
- Cần có dữ liệu giao dịch trong `data/data.csv` để xử lý dữ liệu thực
- API chạy ở chế độ debug để dễ phát triển
- Demo mode tự động tạo dữ liệu mẫu để test
