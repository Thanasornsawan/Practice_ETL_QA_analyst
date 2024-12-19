# Query to Validate Customer_ID Uniqueness
def validate_customer_id_unique():
    return """
        SELECT Customer_ID, Order_Date, COUNT(*) AS Order_Count
        FROM Orders
        GROUP BY Customer_ID, Order_Date
        HAVING COUNT(*) > 1
    """

# Query to Validate Correct Date Format
def validate_order_date_format():
    return """
        SELECT Order_ID, Order_Date
        FROM Orders
        WHERE Order_Date IS NULL
           OR NOT (Order_Date GLOB '????-??-??' 
                   AND LENGTH(Order_Date) = 10
                   AND CAST(substr(Order_Date, 1, 4) AS INTEGER) > 0
                   AND substr(Order_Date, 6, 2) BETWEEN '01' AND '12'
                   AND CASE 
                       WHEN substr(Order_Date, 6, 2) IN ('01', '03', '05', '07', '08', '10', '12') THEN substr(Order_Date, 9, 2) BETWEEN '01' AND '31'
                       WHEN substr(Order_Date, 6, 2) IN ('04', '06', '09', '11') THEN substr(Order_Date, 9, 2) BETWEEN '01' AND '30'
                       WHEN substr(Order_Date, 6, 2) = '02' THEN (
                           CASE 
                               WHEN (CAST(substr(Order_Date, 1, 4) AS INTEGER) % 4 = 0 
                                     AND CAST(substr(Order_Date, 1, 4) AS INTEGER) % 100 != 0) 
                                  OR CAST(substr(Order_Date, 1, 4) AS INTEGER) % 400 = 0 THEN substr(Order_Date, 9, 2) BETWEEN '01' AND '29'
                               ELSE substr(Order_Date, 9, 2) BETWEEN '01' AND '28'
                           END
                       )
                       ELSE 0
                   END = 1
               );
    """

# Query to find orders with negative quantities
def get_orders_with_negative_quantity():
    return """
        SELECT Order_ID, Customer_ID, Product_ID, Quantity
        FROM Orders
        WHERE Quantity < 0
    """

# Query to find orders with missing Customer_Name
def get_orders_with_missing_customer_name():
    return """
        SELECT Order_ID, Customer_ID, Customer_Name, Product_ID, Quantity
        FROM Orders
        WHERE Customer_Name IS NULL
    """

# Query to ensure unique Product_ID (no duplicates allowed in Orders)
def get_orders_with_duplicate_product_id():
    return """
        SELECT Product_ID, COUNT(*) 
        FROM Orders 
        GROUP BY Product_ID 
        HAVING COUNT(*) > 1
    """

# Query to ensure Product_Name cannot be NULL in Products
def get_orders_with_null_product_name():
    return """
        SELECT * 
        FROM Products 
        WHERE Product_Name IS NULL
    """

# Query to get email customer in Orders
def get_invalid_email_customers():
    """
    Query to find customers with invalid email format.
    Returns rows where the email does not match the expected pattern.
    """
    query = """
    SELECT * 
    FROM Orders
    WHERE Email NOT LIKE '%_@__%.__%';
    """
    return query

def get_orders_with_invalid_date_range():
    """
    Query to find orders where the Order_Date is outside the range '2024-01-01' to '2024-12-31'.
    """
    query = """
    SELECT * 
    FROM Orders
    WHERE Order_Date < '2024-01-01' OR Order_Date > '2024-12-31';
    """
    return query

def get_invalid_product_references():
    """
    Returns the SQL query to check for invalid Product_ID references in the Orders table.
    """
    return """
        SELECT o.Order_ID, o.Product_ID
        FROM Orders o
        LEFT JOIN Products p ON o.Product_ID = p.Product_ID
        WHERE p.Product_ID IS NULL;
    """