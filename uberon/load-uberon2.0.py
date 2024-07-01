import pandas as pd
from sqlalchemy import create_engine

# MySQL database configuration
db_username = 'your_username'
db_password = 'your_password'
db_host = 'localhost'  # or your MySQL server IP
db_name = 'your_database_name'

# Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine(f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}')

# Function to import CSV to MySQL
def import_csv_to_mysql(csv_file, table_name):
    try:
        # Read CSV file into pandas DataFrame
        df = pd.read_csv(csv_file)

        # Remove existing table from database (if exists)
        engine.execute(f'DROP TABLE IF EXISTS {table_name}')

        # Write DataFrame to MySQL
        df.to_sql(table_name, con=engine, index=False)

        print(f"CSV file '{csv_file}' imported successfully into MySQL table '{table_name}'.")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    # CSV files to import
    csv_files = {
        'uberon_main_with_children.csv': 'uberon_main_with_children',
        'uberon_main_with_mesh_umls.csv': 'uberon_main_with_mesh_umls'
    }

    # Import each CSV file into MySQL
    for csv_file, table_name in csv_files.items():
        import_csv_to_mysql(csv_file, table_name)
