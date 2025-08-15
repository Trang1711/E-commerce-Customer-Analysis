import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from config import MSSQL_SERVER, MSSQL_DATABASE, MSSQL_USERNAME, MSSQL_PASSWORD, MSSQL_DRIVER

def get_engine():
    server = MSSQL_SERVER
    db = MSSQL_DATABASE
    user = MSSQL_USERNAME
    pwd = MSSQL_PASSWORD
    driver = MSSQL_DRIVER
    params = quote_plus(f"DRIVER={driver};SERVER={server};DATABASE={db};UID={user};PWD={pwd}")
    conn_str = f"mssql+pyodbc:///?odbc_connect={params}"
    return create_engine(conn_str, fast_executemany=True)
