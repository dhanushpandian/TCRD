import pandas as pd

# Load each CSV file into a pandas DataFrame
disease_df = pd.read_csv('disease.csv')
feature_df = pd.read_csv('feature.csv')
nhprotein_df = pd.read_csv('nhprotein.csv')
protein_df = pd.read_csv('protein.csv')
target_df = pd.read_csv('target.csv')
xref_df = pd.read_csv('xref.csv')

def clean_dataframe(df):
    # Example cleaning steps for disease_df
    # Ensure 'id' column exists and drop duplicates based on it
    if 'id' in df.columns:
        df.drop_duplicates(subset=['id'], keep='first', inplace=True)
    
    # Optionally, add more specific cleaning steps for other DataFrames as needed
    # For feature_df, nhprotein_df, protein_df, target_df, xref_df, adjust the subset of columns accordingly
    
    return df

disease_df = clean_dataframe(disease_df)
feature_df = clean_dataframe(feature_df)
nhprotein_df = clean_dataframe(nhprotein_df)
protein_df = clean_dataframe(protein_df)
target_df = clean_dataframe(target_df)
xref_df = clean_dataframe(xref_df)

# Merge DataFrames based on common columns  
merged_df = disease_df \
    .merge(feature_df, left_on='protein_id', right_on='protein_id', how='left') \
    .merge(nhprotein_df, left_on='nhprotein_id', right_on='id', how='left', suffixes=('_disease', '_nhprotein')) \
    .merge(protein_df, left_on='protein_id', right_on='id', how='left', suffixes=('_nhprotein', '_protein')) \
    .merge(target_df, left_on='protein_id', right_on='id', how='left', suffixes=('_protein', '_target')) \
    .merge(xref_df, left_on='protein_id', right_on='protein_id', how='left', suffixes=('_target', '_xref'))

# Save the merged DataFrame to a new CSV file
merged_df.to_csv('merged_autism_data.csv', index=False)

print(merged_df.head())
