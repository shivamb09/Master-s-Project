import pandas as pd

# Define the filenames
file1 = "FFAR_string.txt"
file2 = "geneID_geneSYMBOL.xlsx"
file3 = "FFAR_final.txt"

# Read the gene symbols from file1 into a list
with open(file1, "r") as f:
    gene_symbols = [line.strip() for line in f]

# Read the Excel file into a DataFrame
df = pd.read_excel(file2)

# Filter the DataFrame to include only rows with gene symbols in file1
filtered_df = df[df['gene_symbol'].isin(gene_symbols)]

# Write the result to file3
with open(file3, "w") as f:
    for index, row in filtered_df.iterrows():
        f.write(f"{row['gene_symbol']} ; {row['gene_id']}\n")

print("Results saved in file3.txt")

 
