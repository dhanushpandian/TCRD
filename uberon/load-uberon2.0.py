import mysql.connector

# Database connection parameters
dbhost = 'localhost'
dbname = 'tcrdev'
dbuser = 'root'
pwfile = './tcrd_pass'

# Read database password from file
with open(pwfile, 'r') as file:
    dbpassword = file.read().strip()

# Connect to the database
cnx = mysql.connector.connect(user=dbuser, password=dbpassword, host=dbhost, database=dbname)
cursor = cnx.cursor()

# SQL query to alter the table schema
alter_query = """
ALTER TABLE uberon_main_with_mesh_umls
MODIFY main_uberon_id VARCHAR(50),
MODIFY mesh_ids VARCHAR(256),
MODIFY umls_ids VARCHAR(512);
"""

# Execute the query
cursor.execute(alter_query)

# Commit the changes and close the connection
cnx.commit()
cursor.close()
cnx.close()
