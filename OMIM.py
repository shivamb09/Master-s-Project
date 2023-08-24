import sys
import re

data=[]

with open('genemap2.txt') as f:
    for line in f:
        if line.startswith('#'):
            continue
        line=line.strip('\n')
        valuelist=line.split('\t')
        chromosome = valuelist[0]
        genomicPositionStart = valuelist[1]
        genomicPositionEnd = valuelist[2]
        cytoLocation = valuelist[3]
        computedCytoLocation = valuelist[4]
        mimNumber = valuelist[5]
        geneSymbols = valuelist[6]
        geneName = valuelist[7]
        approvedGeneSymbol = valuelist[8]
        entrezGeneID = valuelist[9]
        ensemblGeneID = valuelist[10]
        comments = valuelist[11]
        phenotypeString = valuelist[12]
        mouse = valuelist[13]
        if not phenotypeString:
             continue
        for phenotype in phenotypeString.split(';'):
                phenotype = phenotype.strip()
                matcher = re.match(r'^(.*),\s(\d{6})\s\((\d)\)(|, (.*))$', phenotype)
                if matcher:
                    phenotype = matcher.group(1)
                    phenotypeMimNumber = matcher.group(2)
                    phenotypeMappingKey = matcher.group(3)
                    inheritances = matcher.group(5)
                    data.append((phenotype,entrezGeneID))
                    
                else:
                     matcher = re.match(r'^(.*)\((\d)\)(|, (.*))$', phenotype)
                     if matcher:
                          phenotype = matcher.group(1)
                          phenotypeMappingKey = matcher.group(2)
                          inheritances = matcher.group(3)
                          data.append((phenotype,entrezGeneID))
        print(data[len(data)-1])  

output_file = 'output.txt'
with open(output_file, 'w') as f:
    for phenotype, entrezGeneID in data:
        f.write(f"{phenotype}: {entrezGeneID}\n")
