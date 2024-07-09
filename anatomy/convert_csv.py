import pandas as pd


excel_file_path = 'anatomy.xlsx' 
csv_file_path = 'anatomy_locatedin.csv'     

df = pd.read_excel(excel_file_path)

#count of rows
# print(df.shape[0])

# non_empty_counts = df.iloc[2].notna().sum()

# count_valid_values = df[df.iloc[:, 2].astype(str).str.len() > 3].shape[0]

# print(f"Number of non-empty columns in row {count_valid_values}")
# df.to_csv(csv_file_path, index=False)

# print(f"Excel file has been converted to CSV and saved as {csv_file_path}.")




# Filter rows where the index 2 column is non-empty

# filtered_df = df[df.iloc[:, 2].notna()]
filtered_df = df[df.iloc[:, 2].astype(str).str.len() > 3]

print(filtered_df)
# print(filtered_df.shape[0])


filtered_df.to_csv(csv_file_path, index=False)
