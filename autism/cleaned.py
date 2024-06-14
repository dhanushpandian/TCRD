import pandas as pd

# Load the data from the provided image
file_path = 'merged_autism_data.csv'
df = pd.read_csv(file_path)

# Define the relevant columns to keep
relevant_columns = [
    'id_x', 'dtype', 'protein_id', 'name_disease', 'did', 
    'description_x', 'id_xref', 'xtype', 'target_id', 'nucleic_acid_id', 'value'
]

# Keep only the relevant columns
df_cleaned = df[relevant_columns]

# Remove duplicate diseases based on 'name_disease' and 'description_x'
df_cleaned = df_cleaned.drop_duplicates(subset=['name_disease', 'description_x'])

# Save the cleaned DataFrame to a CSV file
cleaned_file_path = 'cleaned_autism_data.csv'
df_cleaned.to_csv(cleaned_file_path, index=False)

print(f"Cleaned data saved to {cleaned_file_path}")
