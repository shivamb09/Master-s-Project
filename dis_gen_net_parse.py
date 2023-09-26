data = {}

with open('ALL_genes_merged.txt', 'r') as sample_file:
    for line in sample_file:
        parts = line.strip().split('\t')
        if len(parts) >= 3:
            gene_id = parts[0]
            disease_name = parts[1]
            disease_classes = parts[2].split(';')

            # Filter out disease_classes without 'C'
            valid_disease_classes = [cls for cls in disease_classes if cls.startswith('C')]

            # Skip this line if there are no valid disease classes
            if not valid_disease_classes:
                continue

            # Normalize disease_name by converting it to lowercase
            disease_name = disease_name.lower()

            # Add or append the gene to the corresponding disease_name
            if disease_name not in data:
                data[disease_name] = []
            data[disease_name].append(gene_id)

# Create a new text file for the output
with open('dis_gen_genes.txt', 'w') as output_file:
    for disease_name, genes in data.items():
        genes_str = ', '.join(genes)
        output_file.write(f"{disease_name}: {genes_str}\n")

print("Output saved to output.txt.")





