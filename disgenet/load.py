import csv
import mysql.connector

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'desgenet'
}

# Open database connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# File paths
disease_file_path = "./downloads/disease_associations.tsv"
gene_file_path = "./downloads/gene_associations.tsv"

# Function to insert data from a file
def insert_data(cursor, table_name, file_path, header):
    with open(file_path, 'r', encoding='utf-8') as tsvfile:
        tsv_reader = csv.reader(tsvfile, delimiter='\t')
        
        # Skip header
        next(tsv_reader)
        
        for row in tsv_reader:
            if len(row) == len(header):
                insert_query = f"INSERT INTO {table_name} ({', '.join(header)}) VALUES ({', '.join(['%s'] * len(header))})"
                try:
                    cursor.execute(insert_query, row)
                    conn.commit()
                    print("Row inserted successfully.")
                except mysql.connector.Error as err:
                    print("Error inserting row:", err)
            else:
                print("Error: Mismatch in column count for row:", row)

# Insert data from disease file
print("Inserting data from disease file...")
disease_header = ['diseaseId', 'diseaseName', 'diseaseType', 'diseaseClass', 'diseaseSemanticType', 'NofGenes', 'NofPmids']
insert_data(cursor, "disease_associations", disease_file_path, disease_header)

# Insert data from gene file
print("\nInserting data from gene file...")
gene_header = ['geneId', 'geneSymbol', 'DSI', 'DPI', 'PLI', 'protein_class_name', 'protein_class', 'NofDiseases', 'NofPmids']
insert_data(cursor, "gene_associations", gene_file_path, gene_header)

# Close cursor and connection
cursor.close()
conn.close()
