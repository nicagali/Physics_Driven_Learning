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

# def res_change(G, res_change_vec):

#     res_change_value = 0

#     index_vec = 0

#     for edge in G.edges():

#         res_change_value += G.edges[edge]['resistance'] - res_change_vec[index_vec]

#         res_change_vec[index_vec] = G.edges[edge]['resistance']

#         index_vec += 1

#     return res_change_value, res_change_vec



