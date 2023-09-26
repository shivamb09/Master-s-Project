# Read data from file1 and store it in a dictionary
file1_data = {}
with open('final_genes_for_disease.txt', 'r') as file1:
    for line in file1:
        parts = line.strip().split(': ')
        if len(parts) == 2:
            disease_name = parts[0]
            genes = parts[1].split(', ')
            file1_data[disease_name] = set(genes)

# Read data from file2 and update the dictionary with unique genes
with open('OMIM_genes_mapped_to_mesh.txt', 'r') as file2:
    for line in file2:
        parts = line.strip().split(': ')
        if len(parts) == 2:
            disease_name = parts[0]
            genes = parts[1].split(', ')
            if disease_name in file1_data:
                # Update the set with unique genes
                file1_data[disease_name].update(genes)
            else:
                # Create a new set if disease_name doesn't exist
                file1_data[disease_name] = set(genes)

# Create a new text file for the output
with open('pre_final_genes_for_disease.txt', 'w') as output_file:
    for disease_name, genes in file1_data.items():
        genes_str = ', '.join(sorted(genes))  # Sort genes and join them
        output_file.write(f"{disease_name}: {genes_str}\n")

print("Unique genes saved to output.txt.")
