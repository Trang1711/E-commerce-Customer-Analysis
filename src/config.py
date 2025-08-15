# src/config.py
import os

# Database Configuration
MSSQL_SERVER = os.getenv("MSSQL_SERVER", "localhost")
MSSQL_DATABASE = os.getenv("MSSQL_DATABASE", "ecommerce")
MSSQL_USERNAME = os.getenv("MSSQL_USERNAME", "sa")
MSSQL_PASSWORD = os.getenv("MSSQL_PASSWORD", "Password123!")
MSSQL_DRIVER = os.getenv("MSSQL_DRIVER", "ODBC Driver 17 for SQL Server")

# API Configuration
API_TOKEN = os.getenv("API_TOKEN", "secret123")

# Model Configuration
KMEANS_CLUSTERS = 5
RECOMMENDATION_TOP_N = 10
