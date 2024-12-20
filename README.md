# Practice_ETL_QA_analyst
This project use excel, sql, docker and python (pytest)

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

## Test Plan for Data Quality Testing (unit test)

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
pytest -s tests/test_data_unittest.py::test_invalid_product_id
```
This will run only the test_invalid_product_id test case in tests/test_data_unittest.py.

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
pytest tests/test_data_unittest.py
```

# Example fail result after run test
![date result](https://github.com/Thanasornsawan/Practice_ETL_QA_analyst/blob/main/photos/date_range.png?raw=true)

![map result](https://github.com/Thanasornsawan/Practice_ETL_QA_analyst/blob/main/photos/id_mapping.png?raw=true)

## Data Completeness Testing:

**Objective:** Ensure that all expected data is loaded into the target system without any loss. <br/>
**Test Case:** Compare the record counts between the source and target tables to verify completeness.

**Run the test**
```sh
pytest tests/test_load_correct.py
```
![load result](https://github.com/Thanasornsawan/Practice_ETL_QA_analyst/blob/main/photos/test_load.png?raw=true)

# SCD Type 2 testing
## Proposed Workflow
**1. Raw Source Database (etl.db)**<br/>
- Schema: Customer_ID, Customer_Name, Order_Date, Product_ID, Quantity, Email.<br/>

**2. Dimension Database (etl_dm.db)**<br/>
- Schema: EID (Primary Key), Customer_ID, Customer_Name, Order_Date, Product_ID, Quantity, Email, Start_Date, End_Date, Active.<br/>

**3. Logic in create_dm.py**<br/>
* Check if data exists in the dimension database:<br/>
    * **Non-existent Record:** Insert new data with:<br/>
        * Start_Date = today<br/>
        * End_Date = 9999-12-31<br/>
        * Active = Y<br/>
    * **Existing Record:**<br/>
        * Compare Product_ID, Quantity, Order_Date:<br/>
        * If data is different:<br/>
            * Update the End_Date of the old record to today and set Active = N.<br/>
            * Insert the updated record as a new row with Start_Date = today and Active = Y.<br/>

**4. Verification in Tests**<br/>
* Validate SCD Type 2 logic by filtering EID and comparing historical records.<br/>
* Ensure schema alignment between etl.db and etl_dm.db.<br/>

# Step by step to run test<br/>
**1.Create dimension database only once (first time)**
```sh
python sql/sqlite_db/setup_db.py
```
**2. Load data from source db to target dimension db**
```sh
python sql/sqlite_db/create_dm.py 
```
**The table first time, we can see that it has wrong data from source with duplicate Customer_ID**<br/>
![table first insert](https://github.com/Thanasornsawan/Practice_ETL_QA_analyst/blob/main/photos/table_first_insert.png?raw=true)
<br/>
This file you can run mutltiple times, it will compare source db with target db and check with the same Customer_ID and Order_Id which is primary key from source db to update history data change by put Start_Date, End_Date and Active status
<br/>

**3. Run SCD test case file**
```sh
pytest -s tests/test_scd.py
```
![scd step](https://github.com/Thanasornsawan/Practice_ETL_QA_analyst/blob/main/photos/scd_step.png?raw=true)
<br/>
Then, we update quantity of customer name "Jane Smith" and run create_dm.py again<br/>

![table update](https://github.com/Thanasornsawan/Practice_ETL_QA_analyst/blob/main/photos/table_update.png?raw=true)

![scd result](https://github.com/Thanasornsawan/Practice_ETL_QA_analyst/blob/main/photos/scd_result.png?raw=true)