import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Database configuration
db_config = {
    'host': '68.183.83.1',
    'user': 'root',
    'password': 'tcrd@blr',
    'database': 'S24_clinicaltrials',
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

# Read the CSV file
csv_file_path = "ctg-studies.csv"  # Adjust the path to your CSV file
df = pd.read_csv(csv_file_path)

# Function to insert data into the database
def insert_data(cursor, table_name, data_frame):
    for index, row in data_frame.iterrows():
        insert_query = f"""
        INSERT INTO {table_name} (
            NCT_Number, Study_Title, Study_Status, Conditions, Interventions, 
            Sponsor, Collaborators, Age, Phases, Study_Type
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            Study_Title = VALUES(Study_Title),
            Study_Status = VALUES(Study_Status),
            Conditions = VALUES(Conditions),
            Interventions = VALUES(Interventions),
            Sponsor = VALUES(Sponsor),
            Collaborators = VALUES(Collaborators),
            Age = VALUES(Age),
            Phases = VALUES(Phases),
            Study_Type = VALUES(Study_Type)
        """
        try:
            cursor.execute(insert_query, tuple(row))
            conn.commit()
            print(f"Row {index + 1} inserted/updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting row {index + 1}: {err}")
            print(f"Skipping row {index + 1}.")

# Insert data from the CSV file
print("Inserting data from CSV file...")
insert_data(cursor, "clinical_trials", df)

# Close cursor and connection
cursor.close()
conn.close()
