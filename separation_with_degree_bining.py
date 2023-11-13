import csv,os,time
import random
from collections import defaultdict
import networkx, random
import numpy

###### Network related ######

def get_network(network_file, only_lcc):
    network = create_network_from_sif_file(network_file, use_edge_data = False, delim = ',', include_unconnected=True)
    #print len(network.nodes()), len(network.edges())
    if only_lcc and not network_file.endswith(".lcc"):
        print ("Shrinking network to its LCC", len(network.nodes()), len(network.edges()))
        components = get_connected_components(network, False)
        network = get_subgraph(network, components[0])
        print ("Final shape:", len(network.nodes()), len(network.edges()))
        #print len(network.nodes()), len(network.edges())
        network_lcc_file = network_file + ".lcc"
        if not os.path.exists(network_lcc_file ):
            f = open(network_lcc_file, 'w')
            for u,v in network.edges():
                f.write("%s 1 %s\n" % (u, v))
            f.close()
    return network

def create_network_from_sif_file(network_file_in_sif, use_edge_data = False, delim = ',', include_unconnected=True):
    setNode, setEdge, dictDummy, dictEdge = get_nodes_and_edges_from_sif_file(network_file_in_sif, store_edge_type = use_edge_data, delim = delim)
    g = create_graph()
    if include_unconnected:
        g.add_nodes_from(setNode)
    if use_edge_data:
        for e,w in dictEdge.iteritems():
            u,v = e
            g.add_edge(u,v,w=w) #,{'w':w})
    else:
        g.add_edges_from(setEdge)
    return g

def get_nodes_and_edges_from_sif_file(file_name, store_edge_type = False, delim=',', data_to_float=True):
    """
    Parse sif file into node and edge sets and dictionaries
    returns setNode, setEdge, dictNode, dictEdge
    store_edge_type: if True, dictEdge[(u,v)] = edge_value
    delim: delimiter between elements in sif file, if None all whitespaces between letters are considered as delim
    """
    setNode = set()
    setEdge = set()
    dictNode = {}
    dictEdge = {}
    flag = False
    f=open(file_name)
    for line in f:
        words = line.rstrip("\n").split(',')
        if len(words)!=2: 
            continue
        id1 = words[0]
        setNode.add(id1)
        id2 = words[1]
        setNode.add(id2)
        setEdge.add((id1, id2))
        #if len(words) == 2:
            #if data_to_float:
                #score = float(words[1])
            #else:
                #score = words[1]
            #dictNode[id1] = score
        #elif len(words) >= 3: 
            #if len(words) > 3:
                #flag = True
            #id2 = words[2]
            #setNode.add(id2)
            #setEdge.add((id1, id2))
            #if store_edge_type:
                #if data_to_float:
                    #dictEdge[(id1, id2)] = float(words[1])
                #else:
                    #dictEdge[(id1, id2)] = words[1]
    f.close()
    if len(setEdge) == 0:
        setEdge = None
    if len(dictNode) == 0:
        dictNode = None
    if len(dictEdge) == 0:
        dictEdge = None
    if flag:
        print ("Warning: Ignored extra columns in the file!")
    return setNode, setEdge, dictNode, dictEdge

def create_graph(directed=False):
    """
        Creates & returns a graph
    """
    if directed:
        g = networkx.DiGraph()
    else:
        g = networkx.Graph()
    return g

def get_connected_components(G, return_as_graph_list=True):
    """
        Finds (strongly in the case of directed network) connected components of graph
        returnAsGraphList: returns list of graph objects corresponding to connected components (from larger to smaller)
        otherwise returns list of node list corresponding nodes in connected components
    """
    result_list = []

    if return_as_graph_list:
        result_list = networkx.connected_component_subgraphs(G)
    else:
        result_list = [c for c in sorted(networkx.connected_components(G), key=len, reverse=True)]

    return result_list

def get_subgraph(G, nodes):
    """
    NetworkX subgraph method wrapper
    """
    return G.subgraph(nodes)


###### Random_network related ######

def get_random_nodes(nodes, network, bins=None, n_random=1000, min_bin_size=100, degree_aware=True, seed=None):
    if bins is None:
        # Get degree bins of the network
        bins = get_degree_binning(network, min_bin_size) 
    nodes_random = pick_random_nodes_matching_selected(network, bins, nodes, n_random, degree_aware, seed=seed) 
    return nodes_random

def get_degree_binning(g, bin_size, lengths=None):
    degree_to_nodes = {}
    for node, degree in g.degree(): #.iteritems(): # iterator in networkx 2.0
        if lengths is not None and node not in lengths:
            continue
        degree_to_nodes.setdefault(degree, []).append(node)
    values = sorted(degree_to_nodes.keys())
    bins = []
    i = 0
    while i < len(values):
        low = values[i]
        val = degree_to_nodes[values[i]]
        while len(val) < bin_size:
            i += 1
            if i == len(values):
                break
            val.extend(degree_to_nodes[values[i]])
        if i == len(values):
            i -= 1
        high = values[i]
        i += 1 
        #print i, low, high, len(val) 
        if len(val) < bin_size:
            low_, high_, val_ = bins[-1]
            bins[-1] = (low_, high, val_ + val)
        else:
            bins.append((low, high, val))
    return bins

def pick_random_nodes_matching_selected(network, bins, nodes_selected, n_random, degree_aware=True, connected=False, seed=None):
    """
    Use get_degree_binning to get bins
    """
    if seed is not None:
        random.seed(seed)
    values = []
    nodes = network.nodes()
    for i in range(n_random):
        if degree_aware:
            if connected:
                raise ValueError("Not implemented!")
            nodes_random = set()
            node_to_equivalent_nodes = get_degree_equivalents(nodes_selected, bins, network)
            for node, equivalent_nodes in node_to_equivalent_nodes.items():
                #nodes_random.append(random.choice(equivalent_nodes))
                chosen = random.choice(equivalent_nodes)
                for k in range(20): # Try to find a distinct node (at most 20 times)
                    if chosen in nodes_random:
                        chosen = random.choice(equivalent_nodes)
                nodes_random.add(chosen)
            nodes_random = list(nodes_random)
        else:
            if connected:
                nodes_random = [ random.choice(nodes) ]
                k = 1
                while True:
                    if k == len(nodes_selected):
                        break
                    node_random = random.choice(nodes_random)
                    node_selected = random.choice(network.neighbors(node_random))
                    if node_selected in nodes_random:
                        continue
                    nodes_random.append(node_selected)
                    k += 1
            else:
                nodes_random = random.sample(nodes, len(nodes_selected))
        values.append(nodes_random)
    return values

def get_degree_equivalents(seeds, bins, g):
    seed_to_nodes = {}
    for seed in seeds:
        d = g.degree(seed)
        for l, h, nodes in bins:
            if l <= d and h >= d:
                mod_nodes = list(nodes)
                mod_nodes.remove(seed)
                seed_to_nodes[seed] = mod_nodes
                break
    return seed_to_nodes

###### Separation related ######
def get_separation(network, nodes_from, nodes_to, lengths=None):
    dAA = numpy.mean(get_separation_within_set(network, nodes_from, lengths))
    #print(dAA)
    dBB = numpy.mean(get_separation_within_set(network, nodes_to, lengths))
    #print(dBB)
    dAB = numpy.mean(get_separation_between_sets(network, nodes_from, nodes_to, lengths))
    #print(dAB)
    d = dAB - (dAA + dBB) / 2.0
    #print(d)
    return d

def get_shortest_path_length_between(G, source_id, target_id):
    return networkx.shortest_path_length(G, source_id, target_id)

def get_separation_between_sets(network, nodes_from, nodes_to, lengths=None):
    """
    Calculate dAB in separation metric proposed by Menche et al. 2015
    """
    values = []
    target_to_values = {}
    source_to_values = {}
    for source_id in nodes_from:
        for target_id in nodes_to:
            if lengths is not None:
                d = lengths[source_id][target_id]
            else:
                d = get_shortest_path_length_between(network, source_id, target_id)
            source_to_values.setdefault(source_id, []).append(d)
            target_to_values.setdefault(target_id, []).append(d)
    # Distances to closest node in nodes_to (B) from nodes_from (A)
    for source_id in nodes_from:
        inner_values = source_to_values[source_id]
        values.append(numpy.min(inner_values))
    # Distances to closest node in nodes_from (A) from nodes_to (B)
    for target_id in nodes_to:
        inner_values = target_to_values[target_id]
        values.append(numpy.min(inner_values))
    return values


def get_separation_within_set(network, nodes_from, lengths=None):
    """
    Calculate dAA or dBB in separation metric proposed by Menche et al. 2015
    """
    if len(nodes_from) == 1:
        return [ 0 ]
    values = []
    # Distance to closest node within the set (A or B)
    for source_id in nodes_from:
        inner_values = []
        for target_id in nodes_from:
            if source_id == target_id:
                continue
            if lengths is not None:
                d = lengths[source_id][target_id] 
            else:
                d = get_shortest_path_length_between(network, source_id, target_id)
            inner_values.append(d)
        values.append(numpy.min(inner_values))
    return values

def calculate_separation_proximity(network, nodes_from, nodes_to, nodes_from_random=None, nodes_to_random=None, bins=None, n_random=1000, min_bin_size=100, seed=452456, lengths=None):
    """
    Calculate proximity from nodes_from to nodes_to
    If degree binning or random nodes are not given, they are generated
    lengths: precalculated shortest path length dictionary
    """
    nodes_network = set(network.nodes())
    if len(set(nodes_from) & nodes_network) == 0 or len(set(nodes_to) & nodes_network) == 0:    
        return None # At least one of the node group not in network
    d = get_separation(network, nodes_from, nodes_to, lengths)
    if bins is None and (nodes_from_random is None or nodes_to_random is None):
        bins = get_degree_binning(network, min_bin_size, lengths) # if lengths is given, it will only use those nodes
    if nodes_from_random is None:
        nodes_from_random = get_random_nodes(nodes_from, network, bins = bins, n_random = n_random, min_bin_size = min_bin_size, seed = seed)
    if nodes_to_random is None:
        nodes_to_random = get_random_nodes(nodes_to, network, bins = bins, n_random = n_random, min_bin_size = min_bin_size, seed = seed)
    random_values_list = zip(nodes_from_random, nodes_to_random)
    values = numpy.empty(len(nodes_from_random)) #n_random
    
    for i, values_random in enumerate(random_values_list):
        nodes_from, nodes_to = values_random
        values[i] = get_separation(network, nodes_from, nodes_to, lengths)
        
    m, s = numpy.mean(values), numpy.std(values)
    if s == 0:
        z = 0.0
    else:
        z = (d - m) / s
    return d, z

def calculate_proximity_multiple(network, from_file=None, to_file=None, n_random=1000,min_bin_size=100, seed=452456, lengths=None, out_file="separation_result.txt"):
    """
    Run proximity on each entries of from and to files in a pairwise manner
    output is saved in out_file (e.g., output.txt)
    """
    nodes = set(network.nodes())
    disease_main= get_diseaseA_genes(from_file, nodes = nodes)
    disease_others= get_diseaseB_genes(to_file, nodes = nodes)
    print (len(disease_main), len(disease_others))
    # Get degree binning 
    bins = get_degree_binning(network, min_bin_size)
    f = open(out_file, 'w')
    for diseaseA, nodes_from in disease_main.items():
        for diseaseB, nodes_to in disease_others.items():
            print (diseaseA,diseaseB)            
            d, z = calculate_separation_proximity(network, nodes_from, nodes_to, nodes_from_random=None, nodes_to_random=None, bins=bins, n_random=n_random, min_bin_size=min_bin_size, seed=seed, lengths=lengths)
            f.write("%s\t%s\t%f\t%f\n" % (diseaseA, diseaseB, d, z))
        
    f.close()
    return 

def get_diseaseA_genes(from_file, nodes=None, network=None):
    """
    If nodes is not None, keep only nodes in the network
    If network is not None, keep only LCC
    """
    diseaseA_genes = {}
    diseaseA=[]
    z=open(from_file)
    for line in z:
        words = line.split(":")
        diseaseA= words[0].strip("\n")
        genes_list = [gene.strip() for gene in words[1].split(',')]
        genes=set(genes_list)
        if nodes is not None:
            genes&=nodes
            if len(genes) == 0:
                continue
        if network is not None:
            network_sub = network.subgraph(genes)
            genes =get_connected_components(network_sub, False)[0]
        diseaseA_genes[diseaseA] = genes
    return diseaseA_genes

def get_diseaseB_genes(to_file, nodes=None, network=None):
    """
    If nodes is not None, keep only nodes in the network
    If network is not None, keep only LCC
    """
    diseaseB_genes = {}
    diseaseB=[]
    z=open(to_file)
    for line in z:
        words = line.split(":")
        diseaseB = words[0].strip("\n")
        genes_list = [gene.strip() for gene in words[1].split(',')]
        genes=set(genes_list)
        if nodes is not None:
            genes &= nodes
            if len(genes) == 0:
                continue
        if network is not None:
            network_sub = network.subgraph(genes)
            genes =get_connected_components(network_sub, False)[0]
        diseaseB_genes[diseaseB] = genes
    return diseaseB_genes

print( 'starting time:, ', time.ctime())

network_file="interactome.csv"
network = get_network(network_file, only_lcc = True)
from_file = "PCOS_sindhuja.txt"
to_file = "diseaseome_new_100_genes.txt"
calculate_proximity_multiple(network, from_file, to_file, n_random=1000, min_bin_size=100, seed=452456, lengths=None, out_file="separation_result.txt")
print( 'Ending time:, ', time.ctime())
