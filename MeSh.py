import networkx

def main():
    base_dir = "xyz"                        # the main directory where the file is present            

    rel_file = base_dir + "mtrees2013.txt"  # followed by the file name 
   
    m = MESH(rel_file)                      # object instantiation (class MESH)

    g = m.get_ontology()                    # calling out the function get_ontology to plot a Digraph for the input data(discussed below) and saved in variable g.

    #print len(g.nodes()), len(g.edges())
    #concept = "Mycoses"
    
    concept = "Diabetes Mellitus, Type 2"   # announcing the disease name
    
    concept_ids = m.get_concept_ids(concept)# using get_concept_ids function in class MESH to get the MESH id for the disease
   
    for concept_id in concept_ids:          # iterating in concept_ids to get the edges in the tree connecting to the concept_id(i.e the subtree in the heirarchy)
	print concept_id, g.edges([concept_id])
	for u, v in g.edges([concept_id]):
	    print v, m.get_concept(v)       # u represent the source edge and v represents the target edge , so for target edge we will extarct the disease assosciated with it.
    return

def get_mesh_term_to_tree_ids(rel_file):
    m = MESH(rel_file)
    g = m.get_ontology()
    return m.concept_to_concept_ids

class MESH(object):

    def __init__(self, file_name):          # all the variables have been announced empty 
	self.file_name = file_name
	self.delim = ";"
	self.ontology = None 
	self.concept_to_concept_ids = None
	self.concept_id_to_concept = None
	self.root_concept_ids = None
	return

    def get_concept_ids(self, concept):
	return self.concept_to_concept_ids[concept]

    def get_concept(self, concept_id):
	return self.concept_id_to_concept[concept_id]

    def get_ontology(self):
	if self.ontology is not None:
	    return self.ontology
	self.ontology = networkx.DiGraph()
	self.concept_to_concept_ids = {}     # announcing all of them as empty dicitonary
	self.concept_id_to_concept = {}
	self.root_concept_ids = []
	f = open(self.file_name)
	for line in f:
	    words = line.strip("\n").split(self.delim)
	    concept = words[0]
	    concept_id = words[1]
	    self.concept_id_to_concept[concept_id] = concept
	    self.concept_to_concept_ids.setdefault(concept, []).append(concept_id)     # for making an empty concept_to_concept_ids dictionary we have a list of concept ids for a disease so we first announce concept as a keyword and then append the concept ids to the empty list. 
	    inner_words = concept_id.split(".")
	    if len(inner_words) == 1:
		self.root_concept_ids.append(inner_words[0])                           # This code is part of a conditional statement that checks whether the length of the inner_words list is equal to 1. If the length is 1, it indicates that the current concept is a root concept, meaning it has no parent in the ontology hierarchy.
	    else:
		parent_id = ".".join(inner_words[:-1])                                 #The line of code parent_id = ".".join(inner_words[:-1]) constructs the parent concept ID by joining all elements of the inner_words list except the last one using a dot . as a separator.
                self.ontology.add_edge(parent_id, concept_id)                           Let's break it down step by step:
                self.ontology.add_edge(parent_id, concept_id)
	    return self.ontology                                                        inner_words: This is a list that contains the individual components of the concept_id split using the dot . delimiter. For example, if concept_id is "C0011849.123.456", then inner_words would be ["C0011849", "123", "456"].
                                                                                        inner_words[:-1]: This uses slicing to create a new list that contains all elements of inner_words except the last one. In our example, inner_words[:-1] would be ["C0011849", "123"].
                                                                                        ".".join(inner_words[:-1]): This joins the elements of the sliced inner_words list using the dot . as a separator. In our example, it would produce the string "C0011849.123".
                                                                                        So, in the context of your code, this line is creating the parent_id by combining the first part of the concept_id (representing the parent concept) with the dot-separated components that identify its position in the hierarchy. The resulting parent_id string represents the concept ID of the parent concept in the ontology.
        self.ontology.add_edge(parent_id, concept_id)
	return self.ontology


if __name__ == "__main__":
    main()
