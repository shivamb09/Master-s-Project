# Read disease names from disease_name.txt and convert them to lowercase
with open('diseasenames.txt', 'r') as name_file:
    valid_disease_names = set(line.strip().lower() for line in name_file)

# Initialize a dictionary to store disease-gene mappings
disease_gene_mapping = {}

# Read the sample text and process each line
with open('HPO_genes_final.txt', 'r') as sample_file:
    for line in sample_file:
        parts = line.strip().split(': ')
        if len(parts) == 2:
            disease_name, genes = parts[0].strip().lower(), parts[1]
            if disease_name in valid_disease_names:
                if disease_name in disease_gene_mapping:
                    disease_gene_mapping[disease_name] += f",{genes}"
                else:
                    disease_gene_mapping[disease_name] = genes

# Create a new text file for the output
with open('HPO_genes_mapped_to_meshtxt', 'w') as output_file:
    for disease_name, genes in disease_gene_mapping.items():
        output_file.write(f"{disease_name}: {genes}\n")

print("Matching disease-gene entries saved to output.txt.")




