FROM nouchka/sqlite3:latest

# Set working directory to where the database will reside
WORKDIR /opt/sqlite_db

# Initialize or create the SQLite database
RUN sqlite3 /opt/sqlite_db/etl.db "CREATE TABLE IF NOT EXISTS Orders (Order_ID INTEGER PRIMARY KEY AUTOINCREMENT, Product_Name TEXT, Quantity INTEGER);"
