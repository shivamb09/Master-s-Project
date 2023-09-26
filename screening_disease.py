# Initialize a dictionary to store disease names and their associated genes
disease_genes = {}

# Read the text file and collect disease names and genes
with open('pre_final_genes_for_disease.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(': ')
        if len(parts) == 2:
            disease_name = parts[0]
            genes = parts[1].split(', ')
            disease_genes[disease_name] = genes

# Filter diseases with 15 or more genes
filtered_diseases = {disease: genes for disease, genes in disease_genes.items() if len(genes) >= 15}

# Create a new text file for the output
with open('final_diseases_for_RWR.txt', 'w') as output_file:
    for disease, genes in filtered_diseases.items():
        genes_str = ', '.join(genes)
        output_file.write(f"{disease}: {genes_str}\n")

print("Filtered diseases saved to filtered_output.txt.")
