import networkx as nx
import random
from parameters import *

# Initialize the value of resistance in every edge of the graph G to the 
# value "resistance_value". The function returns the graph G with edges 
# initialized.
def initalize_resistances(G):

    for edge in G.edges():
        G.edges[edge]['resistance'] = initial_value_resistances

    return G

def initialize_conductances(G):

    for edge in G.edges():
        G.edges[edge]['conductance'] = initial_value_conductance

    return G

# Construct the simple graph in Dillavou paper: 3 nodes, 2 external sources
# with voltages [5, 0] and target node in the middle. Resistances initialized
# at R = 50 kOhm
def simple_graph(save_data=False):

    G = nx.Graph()
    
    attributes = {"type" : "source", 'color' : color_dots[0]}
    G.add_node(0, **attributes)
    G.add_node(2, **attributes)
    attributes = {"type" : "target", 'color' : color_dots[1]}
    G.add_node(1, **attributes)

    G.nodes[0]['voltage'] = 5
    G.nodes[2]['voltage'] = 0
    G.nodes[1]['voltage'] = 1

    G.add_edge(0,1)
    G.add_edge(1,2)

    # Initialize resistances
    initalize_resistances(G)

    # Initialize conductances
    initialize_conductances(G)

    # desired_output = 4

    # Save to data folder

    if save_data:

        nx.write_graphml(G, f"/home/monicaconte/nica/phd/Projects/Dillavou/general_network/data/graphs/simple_graph.graphml")

    return G

def two_nodes_graph(save_data=False):

    G = nx.Graph()
    
    attributes = {"type" : "source", 'color' : color_dots[0]}
    G.add_node(0, **attributes)
    
    attributes = {"type" : "target", 'color' : color_dots[1]}
    G.add_node(1, **attributes)

    G.nodes[0]['voltage'] = 5
    
    G.add_edge(0,1)
    
    # Initialize resistances
    initalize_resistances(G)

    # Initialize conductances
    initialize_conductances(G)

    # desired_output = 4

    # Save to data folder

    if save_data:

        nx.write_graphml(G, f"{DATA_PATHG}two_nodes_graph.graphml")

    return G


# Construct a general random network. Specify # of nodes "nodes", # of edges "edges"
# # of source nodes "numb_sources", # of target nodes "numb_targets" and input 
# voltages on sources "volt_sources"
def random_graph(save_data=False, res_change=False):

    nodes = numb_nodes
    edges = numb_edges
    numb_sources = numb_source_nodes
    numb_targets = numb_target_nodes
    volt_sources = source_voltages

    G = nx.gnm_random_graph(nodes, edges)

    # Randomly select sources and targets
    sources = random.sample(G.nodes(), numb_sources)
    target_sampling_list = [x for x in G.nodes() if x not in sources]
    targets = random.sample(target_sampling_list, numb_targets)

    # Assign attributes nodes
    volt_index=0
    for node in range(len(G.nodes)):
        if node in sources:
            G.nodes[node]['type'] = 'source'
            color_index = 0
            G.nodes[node]['color'] = color_dots[color_index]
            G.nodes[node]['voltage'] = volt_sources[volt_index]
            volt_index+=1
        elif node in targets:
            G.nodes[node]['type'] = 'target'
            color_index = 1
            G.nodes[node]['color'] = color_dots[color_index]
        else:
            G.nodes[node]['type'] = 'hidden'
            color_index = 2
            G.nodes[node]['color'] = color_dots[color_index]

    # Initialize resistances
    initalize_resistances(G)

    # Initialize conductances
    initialize_conductances(G)

    if save_data:

        nx.write_graphml(G, f"{DATA_PATHG}random_graph.graphml")

    return G

def dillavou_graph(save_data=False):

    G = nx.Graph()

    attributes = {"type" : "source", 'color' : color_dots[0]}
    G.add_node(0, **attributes)
    G.add_node(1, **attributes)
    G.add_node(2, **attributes)
    attributes = {"type" : "target", 'color' : color_dots[1]}
    G.add_node(3, **attributes)
    G.add_node(4, **attributes)
    G.add_node(5, **attributes)
    attributes = {"type" : "hidden", 'color' : color_dots[2]}
    G.add_node(6, **attributes)
    G.add_node(7, **attributes)
    G.add_node(8, **attributes)

    G.nodes[0]['voltage'] = 5
    G.nodes[1]['voltage'] = 1
    G.nodes[2]['voltage'] = 0

    G.add_edges_from([(0,5), (0,6), (0,7), (6,7), (5,7), (5,6), (3,6), (1,3)])
    G.add_edges_from([(1,6), (1,5), (5,8), (1,8), (1,4), (4,8), (2,4), (2,8)])

    # G.add_edge(0,6)

    initalize_resistances(G)

    # Initialize conductances
    initialize_conductances(G)

    if save_data:

        nx.write_graphml(G, f"{DATA_PATHG}dillavou_graph.graphml")

    return G


