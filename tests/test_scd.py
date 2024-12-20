import sqlite3
import pytest
import pandas as pd
import sys
import os

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.sqlite_db.dbm_queries import (
    get_customers_with_duplicates,
    get_order_history_for_customer,
    get_all_column_names,
    get_active_records_count_per_customer
)

# Fixture to set up and tear down the SQLite connection
@pytest.fixture(scope="module")
def db_connection():
    # Ensure the database file exists
    db_path = os.path.join(os.path.dirname(__file__), "../sql/sqlite_db/etl_dm.db")
    assert os.path.exists(db_path), f"Database file not found at {db_path}"

    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()

def test_only_one_active_record_for_each_customer(db_connection):
    # Use the query from db_queries.py to verify only one active record for each customer
    query = get_active_records_count_per_customer()
    df = pd.read_sql(query, db_connection)

    # Ensure there is only one active record per customer
    for record in df.itertuples():
        customer_id = record.Customer_ID  # Access the Customer_ID by column name
        active_count = record.Active_Count  # Access the Active_Count by the column alias
        assert active_count == 1, f"Multiple active records for Customer_ID {customer_id}"

def test_customer_has_history_data(db_connection):
    # Fetch Order_ID and Customer_ID combinations with historical changes
    query = get_customers_with_duplicates()
    df = pd.read_sql(query, db_connection)

    if df.empty:
        print("No historical changes found (all orders have only one record).")
        assert True  # No historical changes, so the test passes
    else:
        for record in df.itertuples():
            customer_id = record.Customer_ID
            order_id = record.Order_ID

            # Fetch all records for the same Customer_ID and Order_ID
            query = get_order_history_for_customer(customer_id, order_id)
            history = pd.read_sql(query, db_connection)

            # Validate historical continuity and active status
            for i, row in history.iterrows():
                if i > 0:
                    # Ensure previous End_Date matches current Start_Date
                    prev_end_date = history.iloc[i - 1]['End_Date']
                    current_start_date = row['Start_Date']
                    assert prev_end_date == current_start_date, (
                        f"Mismatch in dates for Customer_ID = {customer_id}, Order_ID = {order_id}: "
                        f"End_Date ({prev_end_date}) does not match Start_Date ({current_start_date})"
                    )

                # Ensure only the latest record is active
                if i == len(history) - 1:
                    assert row['Active'] == 'Y', (
                        f"Last record for Customer_ID = {customer_id}, Order_ID = {order_id} is not active"
                    )
                    print(
                        f"✅ PASS: Customer_ID = {customer_id}, Order_ID = {order_id} - "
                        f"New record (EID = {row['EID']}) is active."
                    )
                else:
                    assert row['Active'] == 'N', (
                        f"Inactive record for Customer_ID = {customer_id}, Order_ID = {order_id} not marked as 'N'"
                    )
                    print(
                        f"✅ PASS: Customer_ID = {customer_id}, Order_ID = {order_id} - "
                        f"Old record (EID = {row['EID']}) is inactive."
                    )

def test_schema_matches_source(db_connection):
    # Fetch the actual columns from the source database (etl.db), table 'Orders'
    source_db_path = os.path.join(os.path.dirname(__file__), "../sql/sqlite_db/etl.db")
    source_conn = sqlite3.connect(source_db_path)
    source_cursor = source_conn.cursor()
    source_cursor.execute("PRAGMA table_info(Orders)")  # Get columns for the 'Orders' table
    source_columns = {row[1] for row in source_cursor.fetchall()}  # Column name is at index 1
    source_conn.close()

    # Fetch the actual columns from the dimension database (etl_dm.db), table 'Dimension_Orders'
    query = get_all_column_names()  # Get columns for the 'Dimension_Orders' table
    schema_df = pd.read_sql(query, db_connection)
    dimension_columns = set(schema_df['name'])

    # Define the expected additional columns for the dimension table (etl_dm.db)
    expected_dm_columns = {"Start_Date", "End_Date", "Active", "EID"}

    # Assert that all source columns are present in the dimension table
    assert source_columns <= dimension_columns, f"Some source columns from 'Orders' are missing in 'Dimension_Orders': {source_columns - dimension_columns}"

    # Assert that the dimension table has the expected additional columns (SCD related)
    assert expected_dm_columns <= dimension_columns, f"Dimension schema mismatch: {dimension_columns - expected_dm_columns}"

    print("Schema validation passed.")
