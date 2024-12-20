import pandas as pd
import sqlite3
import pytest
import sys
import os
from datetime import datetime

# Add the root directory of the project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sql.sqlite_db.db_queries import (
    validate_customer_id_unique,
    validate_order_date_format,
    get_orders_with_negative_quantity,
    get_orders_with_missing_customer_name,
    get_orders_with_duplicate_product_id,
    get_orders_with_null_product_name,
    get_invalid_email_customers,
    get_orders_with_invalid_date_range,
    get_invalid_product_references
)

# Fixture to set up and tear down the SQLite connection
@pytest.fixture(scope="module")
def db_connection():
    # Ensure the database file exists
    db_path = os.path.join(os.path.dirname(__file__), "../sql/sqlite_db/etl.db")
    assert os.path.exists(db_path), f"Database file not found at {db_path}"

    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()

# Test case 1: Validate customer id unique
def test_customer_id_unique(db_connection):
    query = validate_customer_id_unique()
    df = pd.read_sql(query, db_connection)
    
    # If df is not empty, print the rows that have duplicates
    if not df.empty:
        print("\nDuplicate Customer_IDs found:")
        print(df)

    # Assert that there are no duplicate orders for the same Customer_ID and Order_Date
    assert df.empty, "Duplicate orders exist:\n" + df.to_string(index=False)

def is_valid_date(date_str):
    """Check if a date string is valid (dd/mm/yyyy)."""
    try:
        # Try parsing the date
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

# Test case 2: Validate date format dd/mm/yyyy format
def test_order_date_format(db_connection):
    # Run the SQL query to fetch orders with invalid date formats
    query = validate_order_date_format()  # Your validation SQL query
    df = pd.read_sql(query, db_connection)  # Fetch the result into a DataFrame
    
    # Strip any unwanted characters like newlines
    df['Order_Date'] = df['Order_Date'].str.replace(r'\n', '').str.strip()

    # Validate if the date is in the correct format and valid
    invalid_dates = df[~df['Order_Date'].apply(is_valid_date)]
    
    # Print out any rows with invalid date formats
    if not invalid_dates.empty:
        print("Orders with invalid date format:", invalid_dates)

    # Assert that there are no invalid dates remaining
    assert invalid_dates.empty, f"There are orders with invalid date formats: {invalid_dates}"

# Test case 3: Validate Missing Customer Name
def test_missing_customer_name(db_connection):
    query = get_orders_with_missing_customer_name()
    df = pd.read_sql(query, db_connection)
    
    missing_customer_name = df['Customer_Name'].isnull().sum()  # Count NaN/None values
    print(f"Number of missing Customer_Name values: {missing_customer_name}")

    # Assert that there are no missing customer names (fail if there are any)
    assert missing_customer_name == 0, f"There are orders with missing Customer_Name: {missing_customer_name}"

# Test case 4: Validate Negative Quantity Orders
def test_negative_quantity(db_connection):
    query = get_orders_with_negative_quantity()
    df = pd.read_sql(query, db_connection)
    
    # Log for debugging
    print("DataFrame loaded from the database:")
    print(df)
    print(f"Negative quantities found: {df[df['Quantity'] < 0]}")

    # Assert that there are NO negative quantities
    negative_quantity_count = (df['Quantity'] < 0).sum()  # Count negative quantities
    assert negative_quantity_count == 0, f"Orders with negative quantity found: {negative_quantity_count}"

# Test case 5: Verify order date range should be within month December only
def test_order_date_range(db_connection):
    """
    Validate that all Order_Date values are within the range '2024-12-01' to '2024-12-31'.
    Invalid dates should also be flagged separately.
    """
    # Query all rows from the Orders table
    cursor = db_connection.cursor()
    cursor.execute("SELECT Order_ID, Order_Date FROM Orders")
    rows = cursor.fetchall()

    invalid_dates = []
    out_of_range_dates = []

    # Process each row
    for row in rows:
        order_id = row[0]
        order_date = row[1]

        # Validate the date format
        try:
            # Parse the date assuming the format is 'DD/MM/YYYY'
            parsed_date = datetime.strptime(order_date, '%d/%m/%Y')
            print(f"Parsed Date: {parsed_date}")  # Debugging output

            # Check if the date is out of the valid range (December 2024)
            if not (datetime(2024, 12, 1) <= parsed_date <= datetime(2024, 12, 31)):
                out_of_range_dates.append((order_id, order_date))
        except ValueError:
            # If the date is invalid, add it to the invalid dates list
            invalid_dates.append((order_id, order_date))

    # Log invalid dates
    if invalid_dates:
        print("\nOrders with invalid date formats:")
        for order_id, invalid_date in invalid_dates:
            print(f"Order_ID: {order_id}, Invalid Date: {invalid_date}")

    # Log out-of-range dates
    if out_of_range_dates:
        print("\nOrders with out-of-range dates:")
        for order_id, out_of_range_date in out_of_range_dates:
            print(f"Order_ID: {order_id}, Out-of-Range Date: {out_of_range_date}")

    # Collect all errors and fail at the end
    errors = []
    # Collect all errors and fail at the end
    if invalid_dates:
        errors.append(f"Invalid date formats: {invalid_dates}")
    if out_of_range_dates:
        errors.append(f"Out-of-range dates: {out_of_range_dates}")

    # Combine errors into a single line for better test summary display
    error_message = " | ".join(errors)
    assert not errors, error_message

# Test case 6: Test invalid email format
def test_invalid_email_format(db_connection):
    """
    Test case to validate that all email addresses in the Orders table are in a valid format.
    """
    query = get_invalid_email_customers()
    df = pd.read_sql(query, db_connection)
    
    # Log for debugging
    print("\nRows with invalid email format:")
    print(df)
    
    # Assert that there are no rows with invalid email formats
    assert df.empty, f"Invalid email addresses found:\n{df.to_string(index=False)}"

# Test case 7: Ensure Unique Product_ID (no duplicates allowed)
def test_unique_product_id_in_order(db_connection):
    query = get_orders_with_duplicate_product_id()
    df = pd.read_sql(query, db_connection)
    
    assert df.empty, "There are duplicate Product_IDs in the Orders table"

# Test case 8: Ensure Product_Name Cannot Be NULL
def test_product_name_not_null(db_connection):
    query = get_orders_with_null_product_name()
    df = pd.read_sql(query, db_connection)
    
    assert df.empty, "There are Products with NULL Product_Name"

# Test case 9: Ensure Product_ID in Orders References a Valid Product_ID in Products
def test_referential_integrity(db_connection):
    """
    Test case to validate referential integrity between Orders and Products tables.
    Expected Behavior
    If all Product_IDs in Orders have matching entries in Products, the query should return no rows.
    If any Product_ID in Orders does not have a match in Products, the query should return those Order_IDs and their invalid Product_IDs.
    """
    query = get_invalid_product_references()
    df = pd.read_sql(query, db_connection)
    
    # Log for debugging
    print("\nRows with invalid Product_ID references:")
    print(df.to_string(index=False) if not df.empty else "No issues found.")
    
    # Assert that there are no rows with invalid Product_ID references
    assert df.empty, f"Referential integrity issues found:\n{df.to_string(index=False)}"
