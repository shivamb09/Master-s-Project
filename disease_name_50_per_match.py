import pandas as pd

excel_file_path = 'ALL_genes_merged2.xlsx'
df = pd.read_excel(excel_file_path)

# Filter rows based on your criteria
df = df.dropna(subset=['disease_class'])  # Remove rows with empty 'disease_class'
df = df[df['disease_class'].str.startswith('C')]  # Remove rows where 'disease_class' doesn't start with 'C'

# Save the updated DataFrame back to the Excel file
df.to_excel(excel_file_path, index=False)


import pandas as pd
from fuzzywuzzy import fuzz

master_df = pd.read_excel("screening_info.xlsx")

excel_df = pd.read_excel("ALL_genes_merged1.xlsx")

def is_match(name, master_names):
    name = name.lower() 
    for master_name in master_names:
        master_name = master_name.lower() 
        similarity = fuzz.token_sort_ratio(name, master_name)
        if similarity >= 50:
            return True
    return False

master_names_set = set(master_df["disease_names"])
entry_terms_set = set(entry_term.strip().lower() for entry_terms in master_df["entry_terms"].str.split(';') for entry_term in entry_terms)

master_names_set.update(entry_terms_set)

excel_df["Matched"] = excel_df["disease_names"].apply(lambda x: is_match(x, master_names_set))

filtered_excel_df = excel_df[excel_df["Matched"]]

filtered_excel_df = filtered_excel_df.drop("Matched", axis=1)

filtered_excel_df.to_excel("filtered_excel_file.xlsx", index=False)


import pandas as pd

# Load your Excel files into DataFrames
df_master = pd.read_excel('disease_name_mesh.xlsx')  # Replace with your master file name
df_excel = pd.read_excel('DGN_disease_names2.xlsx')      # Replace with your Excel file name

# Count the exact matches
exact_matches_count = df_excel['disease_name'].isin(df_master['disease_name']).sum()

print(f'Total exact matches: {exact_matches_count}')


import pandas as pd


df = pd.read_excel('ABC.xlsx')  # Replace with your Excel file name


df_no_duplicates = df.drop_duplicates(subset=['disease_name'])


df_no_duplicates.to_excel('DGN_disease_names2.xlsx', index=False)  # Replace with the desired output file name


import pandas as pd

# Load your Excel files into DataFrames
df_master = pd.read_excel('disease_name_mesh.xlsx')  # Replace with your master file name
df_excel = pd.read_excel('DGN_disease_names2.xlsx')      # Replace with your Excel file name

# Find exact matches
exact_matches = df_excel[df_excel['disease_name'].isin(df_master['disease_name'])]

# Count the exact matches
exact_matches_count = len(exact_matches)

print(f'Total exact matches: {exact_matches_count}')

# Print the disease names that match
if exact_matches_count > 0:
    print('Matching Disease Names:')
    for disease_name in exact_matches['disease_name']:
        print(disease_name)


import pandas as pd

# Load your Excel file into a DataFrame
df = pd.read_excel('DGN_data1.xlsx')  # Replace with the path to your Excel file

# Group the DataFrame by 'disease_name' and aggregate 'geneid' values into a set to remove duplicates
grouped = df.groupby('disease_name')['geneid'].apply(set).reset_index()

# Create a dictionary to store the results
result_dict = {}
for index, row in grouped.iterrows():
    disease_name = row['disease_name']
    gene_ids = ', '.join(map(str, row['geneid']))
    result_dict[disease_name] = gene_ids

# Write the results to a text file
with open('Gene_list_DGN1.txt', 'w') as output_file:
    for disease_name, gene_ids in result_dict.items():
        output_file.write(f'{disease_name}:{gene_ids}\n')
