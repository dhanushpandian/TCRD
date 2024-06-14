import pandas as pd

# Load each CSV file into a pandas DataFrame
disease_df = pd.read_csv('disease.csv')
protein_df = pd.read_csv('protein.csv')

# Select only the essential columns
disease_df = disease_df[['id', 'name', 'description', 'protein_id']]
protein_df = protein_df[['id', 'name', 'description']]

# Clean each DataFrame
disease_df.dropna(subset=['id', 'name', 'protein_id'], inplace=True)
protein_df.dropna(subset=['id', 'name'], inplace=True)

# Merge DataFrames based on protein_id
merged_df = disease_df.merge(protein_df, left_on='protein_id', right_on='id', suffixes=('_disease', '_protein'))

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('simplified_autism_data.csv', index=False)

# Print the first few rows of the cleaned DataFrame
print(merged_df.head())
