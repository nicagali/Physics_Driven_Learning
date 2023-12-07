from scipy.optimize import minimize
from matplotlib.ticker import FuncFormatter
import numpy as np
import networkx as nx
import random
from parameters import *
import analysis

def power_function(G):

    power = 0

    for u, v in G.edges():

        resistance = G[u][v]['resistance']
        voltage_u = G.nodes[u]['voltage']
        voltage_v = G.nodes[v]['voltage']

        if resistance != 'removed':

            power += (1/resistance) * (voltage_u - voltage_v)**2
    
    return power

def objective_function(x, G):

    for node in G.nodes():

        G.nodes[node]['voltage'] = x[node]

    return power_function(G)

def generate_constraint(x, fixed_node, fixed_voltage):

    return x[fixed_node] - fixed_voltage

def constraints_dict(fixed_nodes, fixed_voltages):

    const_dictionary = []

    for fixed_node in fixed_nodes:

        constrain = {'type' : 'eq', 'fun' : generate_constraint, 
                     'args' : (fixed_node, fixed_voltages[fixed_nodes.index(fixed_node)],)}

        const_dictionary.append(constrain)

    return const_dictionary

def minimize_graph(G, state):

    if state=="clamped":
        fixed_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == 'source' 
                       or G.nodes[node]['type'] == 'target']
        fixed_voltages = [G.nodes[node]['voltage'] for node in fixed_nodes]
    if state=="free":
        fixed_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == 'source']
        fixed_voltages = [G.nodes[node]['voltage'] for node in fixed_nodes]
     
    initial_guess = np.zeros(len(G.nodes()))
    initial_guess = [fixed_voltages[fixed_nodes.index(node)] if node in fixed_nodes else 0 for node in G.nodes()]
    
    result = minimize(objective_function, initial_guess, args=(G,), 
                      constraints=constraints_dict(fixed_nodes, fixed_voltages))

    return G

def update_clamped(G):

    index_do = 0

    for node in G.nodes():

        if G.nodes[node]['type'] == 'target':

            G.nodes[node]['voltage'] = eta*(desired_output[index_do]) + (1 - eta) * (G.nodes[node]['voltage'])

    return G

def update_resistances(G_free, G_clamped, rule, update, noise=False):

    for edge in G_free.edges():

        if G_free.edges[edge]['resistance'] != 'removed':

            u, v = edge

            diff_free = np.abs(G_free.nodes[u]['voltage'] - G_free.nodes[v]['voltage'])
            diff_clamped = np.abs(G_clamped.nodes[u]['voltage'] - G_clamped.nodes[v]['voltage'])

            delta_v = diff_clamped-diff_free
            delta_v_sq = diff_clamped**2 - diff_free**2
            sample = 0
            if noise:
                sample = np.random.normal(loc=0.0, scale=standard_dev)
                delta_v += sample
                delta_v_sq += sample*(diff_clamped + diff_free)
            
            if rule == 'discrete':
                if delta_v>tol:

                    G_free.edges[edge]['resistance'] += delta_R

                elif delta_v<-tol:

                    G_free.edges[edge]['resistance'] -= delta_R
            else:

                if update=='resistances':

                    prefac = gamma * (1 / (G_free.edges[edge]['resistance'])**2)

                    delta_R_cont = prefac * (delta_v_sq)

                else:

                    prefac = gamma 

                    delta_g_cont = prefac * (-1) * (delta_v_sq)

                    delta_R_cont = 1/ delta_g_cont

                G_free.edges[edge]['resistance'] += delta_R_cont

            if G_free.edges[edge]['resistance'] < tol:

                # G_free.remove_edge(u,v)

                # G_free.edges[edge]['resistance'] += (-1)*delta_R

                G_free.edges[edge]['resistance'] = 'removed'

    return G_free       #here I update only one graph, the important info is in the edges

def train(G, rule, update, simple=False, noise=False):

    G_free = minimize_graph(G, 'free')

    G_copy = G.copy()

    update_clamped(G_copy)

    G_clamped = minimize_graph(G_copy, 'clamped')

    G = update_resistances(G_free, G_clamped, rule, update, noise)

    voltages_simple=[]
    if simple:
        voltages_simple = [G_free.nodes[1]['voltage'], G_clamped.nodes[1]['voltage']]

    return G, voltages_simple

def training_epoch(G, rule, update, mse=False, 
                   resistances_change=False, voltages_simple=False, noise=False):

    ms_normalization=0

    # open files in data
    if mse:
        mse_file = open(f"{DATA_PATH}mse_{rule}.txt", "w") 

    if resistances_change:
        resistance_change_file = open(f"{DATA_PATH}resistances_change_{rule}.txt", "w") 
    if voltages_simple:
        voltages_simple_change_file = open(f"{DATA_PATH}voltages_simple_change_{rule}.txt", "w") 
        voltages_simple_change_file.write(f"{desired_output[0]}\n")

    print(gamma, eta, iterations)

    # train in steps
    for step in range(iterations):

        if voltages_simple and noise:
            G, voltages_simple = train(G, rule, update, simple=True, noise=True)
        elif voltages_simple and noise==False:
            G, voltages_simple = train(G, rule, update, simple=True, noise=False)
        else:
            train(G, rule, update, noise)

        if mse:

            ms_error_value = analysis.ms_error(G)

            if step == 0:
                
                ms_normalization = ms_error_value
            
            mse_file.write(f"{ms_error_value/ms_normalization}\n")

        if resistances_change:

            for edge in G.edges():

                resistance_change_file.write(f"{G.edges[edge]['resistance']}\t")

            resistance_change_file.write("\n")
            

        if voltages_simple:

            voltages_simple_change_file.write(f"{voltages_simple[0]}\t")
            voltages_simple_change_file.write(f"{voltages_simple[1]}\n")

    return G





    