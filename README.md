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

| **Test Case ID** | **Test Case Description**                           | **Steps to Execute**                                                                                                                                                       | **Expected Result**                                                               | **Business Rule Compliance**                                     | **Risk Level**                   | **Test Data**                                             |
|------------------|-----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------|----------------------------------|-----------------------------------------------------------|
| TC_01            | **Validate Customer_ID Uniqueness**                 | - Insert two orders with the same Customer_ID.<br>- Check if the system raises an error or rejects the second order.                                                        | **Failure**: The system should reject the second order with the same Customer_ID. | Duplicate Customer_ID violates uniqueness in the orders table.  | **Critical** – Affects data integrity. | Customer_ID: 1234 (used for two orders)<br>Order_Date: "2024-12-01"<br>Product_ID: 567<br>Quantity: 2 |
| TC_02            | **Validate Correct Date Format**                    | - Insert an order with an invalid date format (e.g., `12/01/2024` for `Order_Date`).<br>- Attempt to save the order.                                                        | **Failure**: The system should reject the order due to incorrect date format.    | The `Order_Date` must follow a standardized format.             | **High** – Incorrect data can cause parsing issues and errors in reporting. | Customer_ID: 1234<br>Order_Date: "12/01/2024" (invalid format)<br>Product_ID: 567<br>Quantity: 2 |
| TC_03            | **Validate Missing Customer_Name**                  | - Insert an order with a missing `Customer_Name` value.<br>- Attempt to save the order.                                                                                     | **Failure**: The system should reject the order due to missing customer name.    | The `Customer_Name` field is mandatory for all orders.         | **High** – Missing customer information affects order processing and analysis. | Customer_ID: 1234<br>Order_Date: "2024-12-01"<br>Product_ID: 567<br>Quantity: 2 (Customer_Name: NULL) |
| TC_04            | **Validate Negative Quantity**                      | - Insert an order with a negative `Quantity` value.<br>- Attempt to save the order.                                                                                        | **Failure**: The system should reject the order due to invalid quantity.         | `Quantity` must always be a positive number.                    | **High** – Negative quantity violates business logic and can affect financial calculations. | Customer_ID: 1234<br>Order_Date: "2024-12-01"<br>Product_ID: 567<br>Quantity: -5 |
| TC_05            | **Validate Missing Order Date**                     | - Insert an order with a missing `Order_Date` value.<br>- Attempt to save the order.                                                                                       | **Failure**: The system should reject the order due to missing order date.       | `Order_Date` cannot be missing.                                | **Critical** – Missing order dates make the data unusable for time-based analysis. | Customer_ID: 1234<br>Customer_Name: "John Doe"<br>Product_ID: 567<br>Quantity: 2 (Order_Date: NULL) |