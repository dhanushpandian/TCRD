import pandas as pd
import mysql.connector
from mysql.connector import errorcode

# Database configuration
db_config = {
    'host': '68.183.83.1',
    'user': 'root',
    'password': 'tcrd@blr',
    'database': 'S24_BIRD',
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

# Read the TSV file without headers and specify column names
tsv_file_path = "data/meddra_all_indications.tsv"  # Adjust the path to your TSV file
df = pd.read_csv(tsv_file_path, sep='\t', header=None, names=[
    'drug_id', 'umls_as_label', 'source', 'concept_name', 
    'concept_type', 'umls_id', 'meddra_concept_name'
])

# Print column names to check
print("Column names in the TSV file:", df.columns)

# Function to insert data into the database
def insert_data(cursor, table_name, data_frame):
    for index, row in data_frame.iterrows():
        # Skip rows where any critical column is missing
        if pd.isnull(row['drug_id']) or pd.isnull(row['umls_as_label']) or pd.isnull(row['source']) or \
           pd.isnull(row['concept_name']) or pd.isnull(row['concept_type']) or pd.isnull(row['umls_id']) or \
           pd.isnull(row['meddra_concept_name']):
            print(f"Skipping row {index + 1} due to missing data.")
            continue
        
        insert_query = f"""
        INSERT INTO {table_name} (
            drug_id, umls_as_label, source, concept_name, 
            concept_type, umls_id, meddra_concept_name
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            umls_as_label = VALUES(umls_as_label),
            source = VALUES(source),
            concept_name = VALUES(concept_name),
            concept_type = VALUES(concept_type),
            umls_id = VALUES(umls_id),
            meddra_concept_name = VALUES(meddra_concept_name)
        """
        try:
            cursor.execute(insert_query, (
                row['drug_id'], row['umls_as_label'], row['source'], row['concept_name'], 
                row['concept_type'], row['umls_id'], row['meddra_concept_name']
            ))
            conn.commit()
            print(f"Row {index + 1} inserted/updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting row {index + 1}: {err}")
            print(f"Skipping row {index + 1}.")

# Insert data from the TSV file
print("Inserting data from TSV file...")
insert_data(cursor, "meddra_indications", df)  # Replace "meddra_indications" with your actual table name

# Close cursor and connection
cursor.close()
conn.close()
