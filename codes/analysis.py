import networkx as nx
from parameters import *
 

def ms_error(G):

    error = 0
    index_do = 0

    for node in G.nodes():

        if G.nodes[node]['type'] == 'target':

            error += (G.nodes[node]['voltage'] - desired_output[index_do])**2
            index_do+=1

    return error




