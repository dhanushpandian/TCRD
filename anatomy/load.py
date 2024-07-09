import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Database configuration
db_config = {
    'host': '68.183.83.1',
    'user': 'root',
    'password': 'tcrd@blr',
    'database': 'Rose',
    'use_pure': True,
    'ssl_disabled': True  # Disable SSL
}

# Attempt to open database connection
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Successfully connected to the database.")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit(1)

# Define the table schema
table_schema = """
CREATE TABLE IF NOT EXISTS disease_data (
    id VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    located_in TEXT,
    PRIMARY KEY (id)
)
"""

# Create the table
try:
    cursor.execute(table_schema)
    conn.commit()
    print("Table created successfully.")
except mysql.connector.Error as err:
    print(f"Error creating table: {err}")
    cursor.close()
    conn.close()
    exit(1)

# Read the Excel file
excel_file_path = "anatomy.xlsx"
df = pd.read_excel(excel_file_path)

# Function to insert data into the database
def insert_data(cursor, table_name, data_frame):
    for index, row in data_frame.iterrows():
        insert_query = f"""
        INSERT INTO {table_name} (id, name, located_in) 
        VALUES (%s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
        name = VALUES(name), 
        located_in = VALUES(located_in)
        """
        try:
            cursor.execute(insert_query, tuple(row))
            conn.commit()
            print(f"Row {index + 1} inserted/updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting row {index + 1}:", err)

# Insert data from the Excel file
print("Inserting data from Excel file...")
insert_data(cursor, "disease_data", df)

# Close cursor and connection
cursor.close()
conn.close()
