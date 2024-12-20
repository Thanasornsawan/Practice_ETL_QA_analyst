import sqlite3

# Path to SQLite database for dimension table
DM_DB_PATH = 'sql/sqlite_db/etl_dm.db'

# Establish a connection
conn = sqlite3.connect(DM_DB_PATH)
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS Dimension_Orders;')
if not cursor.fetchone():
    # Create the Dimension_Orders table
    cursor.execute('''
        CREATE TABLE Dimension_Orders (
            EID INTEGER PRIMARY KEY AUTOINCREMENT,
            Order_ID INTEGER,
            Customer_ID INTEGER,
            Customer_Name TEXT,
            Order_Date TEXT,
            Product_ID INTEGER,
            Quantity INTEGER,
            Email TEXT,
            Start_Date TEXT,
            End_Date TEXT,
            Active TEXT,
            FOREIGN KEY(Order_ID) REFERENCES Orders(Order_ID)  -- Optional: If you want to relate to source DB Order_ID
        );
    ''')
    print("Dimension_Orders table created successfully.")
else:
    print("Dimension_Orders table already exists. No changes made.")

# Commit changes and close the connection
conn.commit()
conn.close()