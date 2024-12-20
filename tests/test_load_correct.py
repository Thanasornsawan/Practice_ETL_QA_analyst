import pandas as pd
import sqlite3
import os

def test_row_count():
    # Path to SQLite database
    DB_PATH = 'sql/sqlite_db/etl.db'
    print(f"Database path: {DB_PATH}")

    # Establish a connection
    conn = sqlite3.connect(DB_PATH)

    # Path to Excel file
    EXCEL_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../orders_test_data.xlsx'))
    print(f"Excel file path: {EXCEL_FILE_PATH}")
    
    # Read source data from Excel file for both sheets
    source_orders_df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="Orders")
    source_products_df = pd.read_excel(EXCEL_FILE_PATH, sheet_name="Products")
    
    # Drop empty rows in both sheets
    source_orders_df = source_orders_df.dropna(how='all')
    source_products_df = source_products_df.dropna(how='all')
    
    print(f"Source Orders Rows: {len(source_orders_df)}")
    print(f"Source Products Rows: {len(source_products_df)}")

    # Read target data from the database for both tables
    target_orders_df = pd.read_sql_query("SELECT * FROM Orders", conn)
    target_products_df = pd.read_sql_query("SELECT * FROM Products", conn)
    
    print(f"Target Orders Rows: {len(target_orders_df)}")
    print(f"Target Products Rows: {len(target_products_df)}")

    # Validate row count for Orders
    assert len(source_orders_df) == len(target_orders_df), (
        f"Row count mismatch for Orders: Source ({len(source_orders_df)}) vs Target ({len(target_orders_df)})"
    )

    # Validate row count for Products
    assert len(source_products_df) == len(target_products_df), (
        f"Row count mismatch for Products: Source ({len(source_products_df)}) vs Target ({len(target_products_df)})"
    )

    print("Row count validation passed for both Orders and Products.")
    conn.close()
