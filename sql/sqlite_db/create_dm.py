import sqlite3
from datetime import datetime

# Paths to the source and dimension databases
SOURCE_DB_PATH = 'sql/sqlite_db/etl.db'
DM_DB_PATH = 'sql/sqlite_db/etl_dm.db'

def sync_dimension_table():
    today = datetime.now().strftime('%Y-%m-%d')
    max_date = '9999-12-31'

    # Connect to source and dimension databases
    source_conn = sqlite3.connect(SOURCE_DB_PATH)
    source_conn.row_factory = sqlite3.Row  # Enable dictionary-style row access
    dm_conn = sqlite3.connect(DM_DB_PATH)
    dm_conn.row_factory = sqlite3.Row

    source_cursor = source_conn.cursor()
    dm_cursor = dm_conn.cursor()

    # Fetch all columns from the source table schema
    source_cursor.execute("PRAGMA table_info(Orders)")
    source_columns = [row[1] for row in source_cursor.fetchall()]  # Extract column names
    source_columns_str = ", ".join(source_columns)  # Prepare for SELECT query

    # Fetch all columns from the dimension table schema
    dm_cursor.execute("PRAGMA table_info(Dimension_Orders)")
    dimension_columns = {row[1] for row in dm_cursor.fetchall()}  # Get dimension table column names

    # Add missing columns to Dimension_Orders
    missing_columns = set(source_columns) - dimension_columns
    for column in missing_columns:
        dm_cursor.execute(f"ALTER TABLE Dimension_Orders ADD COLUMN {column} TEXT")  # Add as TEXT by default
        print(f"Added missing column {column} to Dimension_Orders")

    # Check if Dimension_Orders table is empty
    dm_cursor.execute("SELECT COUNT(*) FROM Dimension_Orders")
    is_dimension_empty = dm_cursor.fetchone()[0] == 0

    # Fetch all records from the source table
    source_cursor.execute(f"SELECT {source_columns_str} FROM Orders")
    source_data = source_cursor.fetchall()

    if not source_data:
        print("No data found in the source table 'Orders'.")
    else:
        print(f"Fetched {len(source_data)} records from the source table 'Orders'.")

    for record in source_data:
        record_dict = dict(record)  # Convert the row to a dictionary
        order_id = record_dict['Order_ID']

        if is_dimension_empty:
            # If Dimension_Orders table is empty, perform an initial load
            placeholders = ", ".join("?" for _ in source_columns)
            columns_str = ", ".join(source_columns)
            dm_cursor.execute(f'''
                INSERT INTO Dimension_Orders 
                ({columns_str}, Start_Date, End_Date, Active)
                VALUES ({placeholders}, ?, ?, ?)
            ''', (*record, today, max_date, 'Y'))
        else:
            # Check if the record exists in the dimension table by Order_ID
            dm_cursor.execute('''
                SELECT * FROM Dimension_Orders 
                WHERE Order_ID = ? AND Active = 'Y'
            ''', (order_id,))
            existing_record = dm_cursor.fetchone()

            if not existing_record:
                # Insert new record
                placeholders = ", ".join("?" for _ in source_columns)
                columns_str = ", ".join(source_columns)
                dm_cursor.execute(f'''
                    INSERT INTO Dimension_Orders 
                    ({columns_str}, Start_Date, End_Date, Active)
                    VALUES ({placeholders}, ?, ?, ?)
                ''', (*record, today, max_date, 'Y'))
            else:
                # Compare source data with existing data
                existing_record_dict = dict(existing_record)
                changes_detected = any(
                    record_dict[col] != existing_record_dict.get(col)
                    for col in source_columns
                )

                if changes_detected:
                    # Update the existing record's End_Date and set Active to 'N'
                    dm_cursor.execute('''
                        UPDATE Dimension_Orders
                        SET End_Date = ?, Active = 'N'
                        WHERE EID = ?
                    ''', (today, existing_record_dict['EID']))

                    # Insert the updated record
                    placeholders = ", ".join("?" for _ in source_columns)
                    columns_str = ", ".join(source_columns)
                    dm_cursor.execute(f'''
                        INSERT INTO Dimension_Orders 
                        ({columns_str}, Start_Date, End_Date, Active)
                        VALUES ({placeholders}, ?, ?, ?)
                    ''', (*record, today, max_date, 'Y'))

    # Commit changes and close connections
    dm_conn.commit()
    source_conn.close()
    dm_conn.close()

    print("Dimension table synced successfully.")

# Run the sync function
sync_dimension_table()