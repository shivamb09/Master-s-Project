import pandas as pd

# Load your Excel file into a DataFrame
df = pd.read_excel('HPO_disease_gene.xlsx')

# Group the gene IDs by disease name and join them as a comma-separated string
result_df = df.groupby('disease_name')['gene_id'].apply(lambda x: ','.join(x.astype(str).unique())).reset_index()

# Save the result to a text file
with open('HPO_genes_final.txt', 'w') as f:
    for _, row in result_df.iterrows():
        f.write(f"{row['disease_name']}: {row['gene_id']}\n")
