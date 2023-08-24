import numpy as np                   # importing the libraries required for xRWR
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import random

df= pd.read_excel('test_data.xlsx')  # Read the file which contains the data and saved in df 

df=df[df['node1'] != df['node2']]    # Remove the self loops(same values in node1 and node2)

df = df.reset_index(drop=True)       # Reseting the index after removing the self loops

G = nx.from_pandas_edgelist(df, 'node1', 'node2')  # Graph(G) taking edges from node1 to node2

largest_component = max(nx.connected_components(G), key=len)  # Extracting the longest connected component of the main graph(G)

df = df[df.apply(lambda row: row['node1'] in largest_component and row['node2'] in largest_component, axis=1)]    # Updating the df with only the nodes in largest component and removing the isolated nodes


num_nodes1=list(df['node1'])         # nodes in node1 of new df 
num_nodes2=list(df['node2'])         # nodes in node2 of new df
sum=num_nodes1+num_nodes2            # concatinating  the nodes from node1 and node2 to sum

unique_list = []                     # empty list called unique_list
for item in sum:                     # removing the duplicates in the sum(which contains the conacatenated nodes from node1 and node2)
    if item not in unique_list:
        unique_list.append(item)

adj_matrix = pd.DataFrame(0, index=unique_list, columns=unique_list) # empty adjacency matrix with the row and column being the unique list

filtered_df = df[(df['node1'].isin(unique_list)) & (df['node2'].isin(unique_list))] # just a check to see that the values in unique list and new df are same

for row in filtered_df.itertuples(index=False):  # updating the values in the adj_matrix to 1 if there is an edge between node1 value and node2 value
    adj_matrix.at[row.node1, row.node2] = 1
    adj_matrix.at[row.node2, row.node1] = 1

col_sums = np.sum(adj_matrix, axis=0)            # Diagonal matrix

reciprocal_sqrt_col_sums = np.where(col_sums != 0, 1.0 / np.sqrt(col_sums), 0)

D_matrix = np.diag(reciprocal_sqrt_col_sums)

n_adj_matrix= (D_matrix)@(adj_matrix)@(D_matrix) # Normalized adjacency matrix( i will put all these under a function)

n_adj_matrix = n_adj_matrix.astype(np.float64)

seeded_nodes=[678,6231,6490,1017,2492,2065,11036,6821,2176,64375,3973,286749,10413,5869,3643,57706,84909,63892,8555,100507346,9924,100422349,2626,606553,149951,252969,120534,388795,22919,7704,3659,1789,1508,157627,101929229,54984,286046]

p0_matrix1 = np.zeros((len(unique_list), 1), dtype=int)  # the values of seeded nodes updated to 1 in p0_matrix 
for i, node in enumerate(A):
    if node in seeded_nodes:
        p0_matrix1[i, 0] = 1

def sum2one(x):                                          # sum to one for p0_matrix
     global p0_matrix2
     column_sums = np.sum(x, axis=0)
     p0_matrix2 = (x)*(1/ column_sums)
     return p0_matrix2

def random_walk_with_restart(n_adj_matrix, num_steps, restart_prob,epsilon):   # Random walk function
    pt = p0_matrix2.copy()
    global affinity_scores
    affinity_scores = [pt]
    
    for t in range(1, num_steps + 1):
        pt_new = (1 - restart_prob) * np.dot(n_adj_matrix, pt) + restart_prob * p0_matrix2
        np.set_printoptions(precision=8)
        print(f"The affinity score for step {t} is: {pt_new}")
        affinity_scores.append(pt_new)
        if np.all(np.abs(pt_new - pt) < epsilon):
            break
        pt = pt_new

affinity_scores

a=len(affinity_scores)

pt_matrix=affinity_scores[len(affinity_scores)-1]      # affinity scores is a list , so we want the last score to be pt_matrix

def sum2one2(x):                                       # Sum to one on final pT_matrix
     global normalized_matrix
     column_sums = np.sum(x, axis=0)
     normalized_matrix = x / column_sums
     sum_of_elements = np.sum(normalized_matrix, axis=0)
     adjustment = 1.0 - sum_of_elements
     num_columns = x.shape[1]
     normalized_matrix += adjustment / num_columns
     return normalized_matrix







