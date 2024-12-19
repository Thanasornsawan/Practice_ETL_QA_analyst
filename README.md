# Practice_ETL_QA_analyst
This project use Apache Airflow, GitHub action CICD, excel, sql, docker and python

# Scenario user story
Ensure that customer order data is correctly loaded into the database so that I can analyze purchasing patterns.

## Acceptance Criteria:
The ```Customer_ID``` must be unique.<br/>
The ```Product_ID``` must exist in the Products table.<br/>
The ```Quantity``` must not be negative.<br/>
The ```Order_Date``` must be valid and in the correct format (YYYY-MM-DD).<br/>
The ```Customer_Name``` must not be empty.<br/>

## Transformation Logic (ETL):
**Extract**: Data is extracted from Excel files containing order details. <br/>
**Transform**:
Remove leading/trailing spaces from Customer_Name.<br/>
Ensure Order_Date is in the correct format (YYYY-MM-DD).<br/>
Handle missing or invalid values for Quantity (e.g., replace negative values with zero).<br/>
**Load**: Data is loaded into the Orders table in SQLite

## Test Plan

| Test Case ID | Test Case Description                                | Steps to Execute                                                                                                                                                    | Expected Result                                                       | Risk Level                       | Test Data                                                                                                                                          |
|--------------|------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| TC_001       | **Validate Customer ID Uniqueness**                  | - Execute `validate_customer_id_unique` query.<br>- Fetch the results into a DataFrame.<br>- Check for any duplicate `Customer_ID`s.                              | **Failure**: The DataFrame should be empty, indicating no duplicates. | **Critical** – Affects data integrity | Customer_ID: 1234 (used for two orders)<br>Order_Date: "2024-12-01"<br>Product_ID: 567<br>Quantity: 2                                              |
| TC_002       | **Validate Correct Date Format**                     | - Execute `validate_order_date_format` query.<br>- Fetch the results into a DataFrame.<br>- Validate if the `Order_Date` is in the correct format (`dd/mm/yyyy`).  | **Failure**: The DataFrame should have no invalid date formats.       | **High** – Affects date parsing and reporting | Customer_ID: 1234<br>Order_Date: "12/01/2024" (invalid format)<br>Product_ID: 567<br>Quantity: 2                                                  |
| TC_003       | **Validate Missing Customer Name**                   | - Execute `get_orders_with_missing_customer_name` query.<br>- Fetch the results into a DataFrame.<br>- Check for any missing `Customer_Name` values.               | **Failure**: There should be no missing customer names.               | **High** – Affects order processing | Customer_ID: 1234<br>Order_Date: "2024-12-01"<br>Product_ID: 567<br>Quantity: 2 (Customer_Name: NULL)                                           |
| TC_004       | **Validate Negative Quantity Orders**                | - Execute `get_orders_with_negative_quantity` query.<br>- Fetch the results into a DataFrame.<br>- Check for negative `Quantity` values.                           | **Failure**: The DataFrame should have no rows with negative quantities. | **High** – Affects business logic and financial calculations | Customer_ID: 1234<br>Order_Date: "2024-12-01"<br>Product_ID: 567<br>Quantity: -5                                                                 |
| TC_005       | **Validate Order Date Range (December 2024 only)**   | - Execute the query to fetch all `Order_ID` and `Order_Date` from the `Orders` table.<br>- Check each order's date format and ensure it's within the range `2024-12-01` to `2024-12-31`.<br>- Identify invalid or out-of-range dates. | **Failure**: Orders with `Order_Date` outside the range `2024-12-01` to `2024-12-31` should be flagged.<br>**Failure**: Orders with invalid date formats should be flagged. | **High** – Invalid or out-of-range dates can affect reporting and processing. | Customer_ID: 1234<br>Order_Date: "01/12/2024"<br>Product_ID: 567<br>Quantity: 10 (Valid date)<br>Customer_ID: 5678<br>Order_Date: "01/11/2024" (Out of range)<br>Customer_ID: 91011<br>Order_Date: "InvalidDate" (Invalid format) |                                                     |
| TC_006       | **Validate Invalid Email Format**                    | - Execute `get_invalid_email_customers` query.<br>- Fetch the results into a DataFrame.<br>- Check for invalid email formats.                                       | **Failure**: The DataFrame should have no rows with invalid emails.   | **High** – Affects customer communication | Customer_ID: 1234<br>Order_Date: "2024-12-01"<br>Product_ID: 567<br>Quantity: 2<br>Customer_Email: "invalid_email"                               |
| TC_007       | **Ensure Unique Product_ID in Order**                | - Execute `get_orders_with_duplicate_product_id` query.<br>- Fetch the results into a DataFrame.<br>- Check for duplicate `Product_ID`s in orders.                  | **Failure**: The DataFrame should be empty, indicating no duplicates. | **Critical** – Affects data integrity | Customer_ID: 1234<br>Order_Date: "2024-12-01"<br>Product_ID: 567 (duplicate)<br>Quantity: 2                                                   |
| TC_008       | **Ensure Product_Name Cannot Be NULL**                | - Execute `get_orders_with_null_product_name` query.<br>- Fetch the results into a DataFrame.<br>- Check for any `NULL` values in `Product_Name`.                  | **Failure**: The DataFrame should have no rows with NULL `Product_Name`. | **High** – Affects order completeness | Customer_ID: 1234<br>Order_Date: "2024-12-01"<br>Product_ID: 567<br>Quantity: 2<br>Product_Name: NULL                                         |
| TC_009       | **Validate Referential Integrity Between Orders and Products** | - Execute `get_invalid_product_references` query.<br>- Fetch the results into a DataFrame.<br>- Check for any `Product_ID` references that do not exist in Products. | **Failure**: The DataFrame should have no rows indicating invalid `Product_ID` references. | **Critical** – Affects data integrity | Customer_ID: 1234<br>Order_Date: "2024-12-01"<br>Product_ID: 999 (non-existing)<br>Quantity: 2                                               |

## To run a specific test case:
**Run by exact function name:**
```sh
pytest -s tests/test_etl.py::test_invalid_product_id
```
This will run only the test_invalid_product_id test case in tests/test_etl.py.

## Running the Project Locally

**1.Create and Activate a Virtual Environment**
```sh
python3 -m venv venv
```

Activate the virtual environment:
```sh
source venv/bin/activate
```

**2.Install Project Dependencies**
```sh
pip install -r requirements.txt
```

**3.Docker step**
```sh
docker-compose down
docker-compose up -d
```

**4.Set Up the Database**
```sh
python sql/sqlite_db/setup_db.py
```

**5.Load Data into the Database**
```sh
python tests/load_data.py
```

**6.Run the test**
```sh
pytest tests/test_etl.py
```