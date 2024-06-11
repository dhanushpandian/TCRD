import os
import requests
import mysql.connector
import csv

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'gwas'
}

# URL and file path configurations
url = "https://www.ebi.ac.uk/gwas/api/search/downloads/full"
save_dir = "./downloads"
filename = "gwas_catalog.tsv"

def download_file(url, save_dir, filename):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    local_path = os.path.join(save_dir, filename)

    print(f"Starting download from {url}")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    
    print(f"File downloaded and saved to {local_path}")
    return local_path

def insert_data_into_db(file_path, db_config):
    # Connect to the database
    print("Connecting to the database")
    conn = mysql.connector.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )
    cursor = conn.cursor()

    # Define the insert query
    insert_query = """
    INSERT INTO gwas_catalog (
        date_added_to_catalog, pubmedid, first_author, date, journal, link, study,
        disease_trait, initial_sample_size, replication_sample_size, region, chr_id, chr_pos,
        reported_genes, mapped_gene, upstream_gene_id, downstream_gene_id, snp_gene_ids,
        upstream_gene_distance, downstream_gene_distance, strongest_snp_risk_allele, snps,
        merged, snp_id_current, context, intergenic, risk_allele_frequency, p_value, pvalue_mlog,
        p_value_text, or_beta, ci_text, platform, cnv
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Read the TSV file and insert data into the database
    print(f"Opening file {file_path}")
    with open(file_path, 'r',encoding='utf-8') as file:
        tsv_reader = csv.reader(file, delimiter='\t')
        header = next(tsv_reader)  # Skip the header row
        
        row_count = 0
        for row in tsv_reader:
            row_count += 1
            print(f"Inserting row {row_count}")
            try:
                # Convert empty strings to None
                row = [None if cell == '' else cell for cell in row]
                cursor.execute(insert_query, row)
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print(f"Problematic row: {row}")

    conn.commit()
    print(f"Data inserted successfully. Total rows inserted: {row_count}")
    cursor.close()
    conn.close()

if __name__ == '__main__':
    #file_path = download_file(url, save_dir, filename)
    file_path = "./downloads/gwas_catalog.tsv"
    insert_data_into_db(file_path, db_config)
