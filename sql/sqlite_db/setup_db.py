import sqlite3

# Path to SQLite database
DB_PATH = 'sql/sqlite_db/etl.db'

# Establish a connection
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop tables if they exist to ensure schema updates
cursor.execute('DROP TABLE IF EXISTS Orders;')
cursor.execute('DROP TABLE IF EXISTS Products;')

# Create the Orders table with the updated schema (including Email column)
cursor.execute('''
    CREATE TABLE Orders (
        Order_ID INTEGER PRIMARY KEY,
        Customer_ID INTEGER,
        Customer_Name TEXT,
        Order_Date TEXT,
        Product_ID INTEGER,
        Quantity INTEGER,
        Email TEXT
    );
''')

# Create the Products table
cursor.execute('''
    CREATE TABLE Products (
        Product_ID INTEGER PRIMARY KEY,
        Product_Name TEXT
    );
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables set up successfully.")
