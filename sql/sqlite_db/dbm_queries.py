def get_customers_with_duplicates():
    """
    Query to check for the same Order_ID and Customer_ID with multiple EID entries.
    """
    return """
        SELECT Customer_ID, Order_ID, COUNT(*) AS Record_Count
        FROM Dimension_Orders
        GROUP BY Customer_ID, Order_ID
        HAVING COUNT(*) > 1
    """

def get_order_history_for_customer(customer_id, order_id):
    """
    Query to fetch all records for a specific Customer_ID and Order_ID.
    """
    return f"""
        SELECT EID, Start_Date, End_Date, Active
        FROM Dimension_Orders
        WHERE Customer_ID = {customer_id} AND Order_ID = {order_id}
        ORDER BY Start_Date ASC
    """

def get_all_column_names():
    """Query to get column names of the Dimension_Orders table"""
    return """
        PRAGMA table_info(Dimension_Orders)
    """

def get_active_records_count_per_customer():
    """Query to verify only one active record for each Customer_ID and Order_ID combination"""
    return """
        SELECT Customer_ID, Order_ID, COUNT(*) AS Active_Count 
        FROM Dimension_Orders 
        WHERE Active = 'Y' 
        GROUP BY Customer_ID, Order_ID
        HAVING COUNT(*) = 1
    """