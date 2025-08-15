# demo_data_processor.py - Xử lý dữ liệu demo cho ecommerce
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import json

def load_and_process_data(file_path="data/data.csv"):
    """Load và xử lý dữ liệu từ CSV file"""
    try:
        # Đọc dữ liệu CSV
        print(f"📁 Đang đọc dữ liệu từ {file_path}...")
        df = pd.read_csv(file_path)
        
        print(f"✅ Đã load thành công {len(df)} dòng dữ liệu")
        print(f"📊 Các cột có sẵn: {list(df.columns)}")
        
        # Hiển thị thông tin cơ bản
        print(f"\n📈 Thông tin dữ liệu:")
        print(f"   - Kích thước: {df.shape}")
        print(f"   - Kiểu dữ liệu:\n{df.dtypes}")
        print(f"   - Giá trị null:\n{df.isnull().sum()}")
        
        return df
        
    except FileNotFoundError:
        print(f"❌ Không tìm thấy file {file_path}")
        return None
    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {e}")
        return None

def create_demo_insights(df):
    """Tạo insights demo từ dữ liệu thực"""
    if df is None:
        print("❌ Không có dữ liệu để xử lý")
        return
    
    print("\n🔍 Tạo insights demo...")
    
    # Giả sử có các cột cơ bản
    if 'customer_id' in df.columns:
        print(f"👥 Số lượng khách hàng duy nhất: {df['customer_id'].nunique()}")
    
    if 'product_id' in df.columns:
        print(f"🛍️ Số lượng sản phẩm duy nhất: {df['product_id'].nunique()}")
    
    if 'amount' in df.columns or 'price' in df.columns:
        amount_col = 'amount' if 'amount' in df.columns else 'price'
        print(f"💰 Tổng doanh thu: {df[amount_col].sum():,.0f}")
        print(f"💰 Doanh thu trung bình: {df[amount_col].mean():,.0f}")
    
    # Tạo sample data cho demo
    create_sample_data()

def create_sample_data():
    """Tạo dữ liệu mẫu cho demo"""
    print("\n🎯 Tạo dữ liệu mẫu cho demo...")
    
    # Tạo dữ liệu khách hàng mẫu
    sample_customers = []
    for i in range(1, 21):
        customer = {
            "customer_id": f"C{i:03d}",
            "recency_days": np.random.randint(1, 365),
            "frequency": np.random.randint(1, 50),
            "monetary": np.random.randint(100, 5000),
            "age": np.random.randint(18, 70),
            "gender": np.random.choice(["Nam", "Nữ"]),
            "city": np.random.choice(["Hà Nội", "TP.HCM", "Đà Nẵng", "Hải Phòng", "Cần Thơ"])
        }
        sample_customers.append(customer)
    
    # Tạo dữ liệu sản phẩm mẫu
    categories = ["Electronics", "Clothing", "Home", "Books", "Sports", "Beauty"]
    sample_products = []
    for i in range(1, 31):
        product = {
            "product_id": f"P{i:03d}",
            "name": f"Sản phẩm {i}",
            "category": np.random.choice(categories),
            "price": np.random.randint(50, 2000),
            "rating": round(np.random.uniform(3.0, 5.0), 1),
            "stock": np.random.randint(0, 100)
        }
        sample_products.append(product)
    
    # Tạo dữ liệu giao dịch mẫu
    sample_transactions = []
    for i in range(100):
        transaction = {
            "transaction_id": f"T{i+1:04d}",
            "customer_id": np.random.choice([c["customer_id"] for c in sample_customers]),
            "product_id": np.random.choice([p["product_id"] for p in sample_products]),
            "quantity": np.random.randint(1, 5),
            "amount": np.random.randint(100, 2000),
            "date": pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(0, 365))
        }
        sample_transactions.append(transaction)
    
    # Lưu dữ liệu mẫu
    sample_data = {
        "customers": sample_customers,
        "products": sample_products,
        "transactions": sample_transactions
    }
    
    with open("demo_data.json", "w", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ Đã tạo dữ liệu mẫu:")
    print(f"   - {len(sample_customers)} khách hàng")
    print(f"   - {len(sample_products)} sản phẩm")
    print(f"   - {len(sample_transactions)} giao dịch")
    print(f"   - Lưu vào file: demo_data.json")

def analyze_customer_segments():
    """Phân tích segments khách hàng"""
    print("\n🎯 Phân tích segments khách hàng...")
    
    try:
        # Đọc dữ liệu mẫu
        with open("demo_data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        customers_df = pd.DataFrame(data["customers"])
        
        # Chuẩn bị dữ liệu cho clustering
        features = ['recency_days', 'frequency', 'monetary']
        X = customers_df[features].values
        
        # Chuẩn hóa dữ liệu
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # K-means clustering
        kmeans = KMeans(n_clusters=4, random_state=42)
        customers_df['segment'] = kmeans.fit_predict(X_scaled)
        
        # Đặt tên segments
        segment_names = {
            0: "At Risk",
            1: "Regular", 
            2: "VIP",
            3: "New Customer"
        }
        customers_df['segment_name'] = customers_df['segment'].map(segment_names)
        
        # Thống kê segments
        segment_stats = customers_df.groupby('segment_name').agg({
            'recency_days': ['mean', 'count'],
            'frequency': 'mean',
            'monetary': 'mean'
        }).round(2)
        
        print("📊 Phân tích segments:")
        print(segment_stats)
        
        # Lưu kết quả
        customers_df.to_csv("customer_segments.csv", index=False)
        print("✅ Đã lưu kết quả phân tích vào customer_segments.csv")
        
        return customers_df
        
    except Exception as e:
        print(f"❌ Lỗi khi phân tích segments: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Khởi động Ecommerce Data Processor...")
    
    # 1. Load và xử lý dữ liệu thực
    df = load_and_process_data()
    
    # 2. Tạo insights demo
    create_demo_insights(df)
    
    # 3. Phân tích segments
    segments_df = analyze_customer_segments()
    
    print("\n🎉 Hoàn thành xử lý dữ liệu!")
    print("📁 Các file đã tạo:")
    print("   - demo_data.json: Dữ liệu mẫu")
    print("   - customer_segments.csv: Kết quả phân tích segments")
