from scipy.optimize import minimize
from matplotlib.ticker import FuncFormatter
import numpy as np
import networkx as nx
import random
from parameters import *
import analysis
import matplotlib.pyplot as plt

def power_function_res(G):

    power = 0

    for u, v in G.edges():

        resistance = G[u][v]['resistance']
        conductance = G[u][v]['conductance']
        voltage_u = G.nodes[u]['voltage']
        voltage_v = G.nodes[v]['voltage']

        if resistance != 'removed':
            power += (1/resistance) * (voltage_u - voltage_v)**2

    return power

def power_function_cond(G):

    power = 0

    for u, v in G.edges():

        conductance = G[u][v]['conductance']
        voltage_u = G.nodes[u]['voltage']
        voltage_v = G.nodes[v]['voltage']

        power += conductance * (voltage_u - voltage_v)**2

    return power

def minimizing_function(x, G):

    G.nodes[1]["voltage"] = x

    power = 0

    for u, v in G.edges():

        conductance = G[u][v]['conductance']
        voltage_u = G.nodes[u]['voltage']
        voltage_v = G.nodes[v]['voltage']

        power += conductance * (voltage_u - voltage_v)**2

    return power

def objective_function_res(x, G):

    for node in G.nodes():

        G.nodes[node]['voltage'] = x[node]

    return power_function_res(G)

def objective_function_cond(x, G):

    for node in G.nodes():

        G.nodes[node]['voltage'] = x[node]

    return power_function_cond(G)

def generate_constraint(x, fixed_node, fixed_voltage):
    
    fixed_node = int(fixed_node)

    return x[fixed_node] - fixed_voltage

def constraints_dict(fixed_nodes, fixed_voltages):

    const_dictionary = []

    for fixed_node in fixed_nodes:

        # print(fixed_node, fixed_voltages[fixed_nodes.index(fixed_node)])

        constrain = {'type' : 'eq', 'fun' : generate_constraint, 
                     'args' : (fixed_node, fixed_voltages[fixed_nodes.index(fixed_node)],)}

        const_dictionary.append(constrain)

    return const_dictionary

def minimize_graph(G, state, update):

    if state=="clamped":
        fixed_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == 'source' 
                       or G.nodes[node]['type'] == 'target']
        fixed_voltages = [G.nodes[node]['voltage'] for node in fixed_nodes]
    if state=="free":
        fixed_nodes = [node for node in G.nodes() if G.nodes[node]['type'] == 'source']
        fixed_voltages = [G.nodes[node]['voltage'] for node in fixed_nodes]

    initial_guess = np.zeros(len(G.nodes()))
    initial_guess = [fixed_voltages[fixed_nodes.index(node)] if node in fixed_nodes else 0 for node in G.nodes()]

    if update == 'resistances':
        result = minimize(objective_function_res, initial_guess, args=(G, ), 
                      constraints=constraints_dict(fixed_nodes, fixed_voltages))
    else:
        result = minimize(objective_function_cond, initial_guess, args=(G, ), 
                      constraints=constraints_dict(fixed_nodes, fixed_voltages), tol=1e-22)
    
    return G

def update_clamped(G, update):

    eta = 0

    if update == 'resistances':

        eta = eta_r

    else:

        eta = eta_c

    index_do = 0


    for node in G.nodes():

        if G.nodes[node]['type'] == 'target':

            G.nodes[node]['voltage'] = eta*(desired_output[index_do]) + (1 - eta) * (G.nodes[node]['voltage'])

    return G

def update_resistances(G_free, G_clamped, rule, noise=False):

    for edge in G_free.edges():

        if G_free.edges[edge]['resistance'] != 'removed':

            u, v = edge

            diff_free = np.abs(G_free.nodes[u]['voltage'] - G_free.nodes[v]['voltage'])
            diff_clamped = np.abs(G_clamped.nodes[u]['voltage'] - G_clamped.nodes[v]['voltage'])

            delta_v = diff_clamped-diff_free
            delta_v_sq = diff_clamped**2 - diff_free**2
            
            sample = 0
            if noise:

                # sample = np.random.normal(loc=0.0, scale=standard_dev)
                sample = 2* np.random.rand() * standard_dev - standard_dev/2
                delta_v += sample
                delta_v_sq += sample*(diff_clamped + diff_free)
            
            if rule == 'discrete':
                if delta_v>tol:

                    G_free.edges[edge]['resistance'] += delta_R

                elif delta_v<-tol:

                    G_free.edges[edge]['resistance'] -= delta_R
                    
                if G_free.edges[edge]['resistance'] < delta_R:
                    
                    G_free.edges[edge]['resistance'] = delta_R
                    
                if G_free.edges[edge]['resistance'] > 100:
                    
                    G_free.edges[edge]['resistance'] = 100
                                    
            else:

                prefac = gamma_r * (1 / (G_free.edges[edge]['resistance'])**2)

                delta_R_cont = prefac * (delta_v_sq)

                G_free.edges[edge]['resistance'] += delta_R_cont

                # if G_free.edges[edge]['resistance'] < 0 or G_free.edges[edge]['resistance']>100:

                #     # G_free.remove_edge(u,v)

                #     G_free.edges[edge]['resistance'] -= delta_R_cont
                    
                
                # G_free.edges[edge]['resistance'] = 'removed'

    return G_free       #here I update only one graph, the important info is in the edges

def update_conductances(G_free, G_clamped, rule):

    G_out = G_free.copy(as_view=False)

    for edge in G_out.edges():

        u, v = edge

        diff_free = np.abs(G_free.nodes[u]['voltage'] - G_free.nodes[v]['voltage'])
        diff_clamped = np.abs(G_clamped.nodes[u]['voltage'] - G_clamped.nodes[v]['voltage'])

        delta_v = diff_clamped-diff_free
        # print(f"Difference clamped - free edge {edge}", delta_v)
        delta_v_sq = diff_clamped**2 - diff_free**2
        # print(f"Difference clamped - free edge {edge} squared", delta_v_sq)

        if rule == 'discrete':
                if delta_v>tol:

                    G_out.edges[edge]['conductance'] -= delta_g

                if delta_v<-tol:

                    G_out.edges[edge]['conductance'] += delta_g
        else:

            delta_g_cont = gamma_c * (-1) * (delta_v_sq)

            G_out.edges[edge]['conductance'] += delta_g_cont
            
            # if G_out.edges[edge]['conductance']<tol:
                
            #     G_out.edges[edge]['conductance'] -= delta_g_cont

            # print("deltag = ", delta_g_cont)

    return G_out       #here I update only one graph, the important info is in the edges

def update_conductances_new(G, state):

    for edge in G.edges():

        u, v = edge

        diff = np.abs(G.nodes[u]['voltage'] - G.nodes[v]['voltage'])

        diff_sq = diff**2

        prefac = gamma_c

        if state=='clamped':

            prefac *= (-1)

        delta_g_cont = prefac * (diff_sq)

        G.edges[edge]['conductance'] += delta_g_cont

    return G     

def train(G, rule, update, noise=False, simple=False):


    G_free = minimize_graph(G, 'free', update)

    G_free = G_free.copy(as_view=False)

    G = update_clamped(G, update)

    G_clamped = minimize_graph(G, 'clamped', update)

    if update=='resistances':
        G = update_resistances(G_free, G_clamped, rule, noise)
    else:
        G = update_conductances(G_free, G_clamped, rule)
        
    voltages_simple=[]
    if simple:
        voltages_simple = [G_free.nodes[1]['voltage'], G_clamped.nodes[1]['voltage']]

    return G, voltages_simple

def train_new_rule(G, update):

    minimize_graph(G, 'free', update)

    update_conductances_new(G, state='free')

    update_clamped(G, update)

    minimize_graph(G, 'clamped', update)

    update_conductances_new(G, state='clamped')
    
    return G

def print_parameters():

    print('General Parameters: \n')
    print('iterations:', f'{iterations},' , 'tollerance on potential difference=', tol, '\n')

    print('Parameters Resistance Update: \n')
    print( f'eta_r = {eta_r},', f'alpha_r = {alpha_r},', 
          f'gamma_r = {gamma_r},', 
          f'initial resistance={initial_value_resistances}', '\n')

    print('Parameters Conductance Update: \n')
    print( f'eta_c = {eta_c},', f'alpha_c = {alpha_c},', 
          f'gamma_c = {gamma_c},', 
          f'initial conductances={initial_value_conductance}', '\n')

def training_epoch(G, rule, update, eta_specify=0, mse=False, resistances_change=False, 
                   conductances_change=False, voltages_simple=False, 
                   noise=False, show_parameters=False, new_rule=False):

    ms_normalization=0
    # open files in data
    if mse and new_rule==False and eta_specify==0:
        mse_file = open(f"{DATA_PATH}mse_{rule}_{update}.txt", "w") 
    if mse and new_rule==False and eta_specify!=0:
        mse_file = open(f"{DATA_PATH}mse_{rule}_{update}_{eta_specify}.txt", "w") 
    if mse and new_rule:
        mse_file = open(f"{DATA_PATH}mse_{rule}_{update}_newrule.txt", "w") 
    if resistances_change:
        resistance_change_file = open(f"{DATA_PATH}resistances_change_{rule}.txt", "w") 
    if conductances_change:
        conductances_change_file = open(f"{DATA_PATH}conductances_change.txt", "w") 
    if voltages_simple:
        voltages_simple_change_file = open(f"{DATA_PATH}voltages_simple_change_{rule}_{update}.txt", "w") 
        voltages_simple_change_file.write(f"{desired_output[0]}\n")
    if show_parameters:
        print_parameters()

    # train in steps
    for step in range(iterations):

        if voltages_simple and noise:
            G, voltages_simple = train(G, rule, update, simple=True, noise=True)
        elif voltages_simple and noise==False:

            G, voltages_simple = train(G, rule, update, simple=True, noise=False)
        else:
            if new_rule:

                G = train_new_rule(G, update)

            else:

                G, voltages_simple = train(G, rule, update)

        if mse:

            ms_error_value = analysis.ms_error(G)

            if step == 0:
                
                ms_normalization = ms_error_value
            
            mse_file.write(f"{ms_error_value/ms_normalization}\n")

        if resistances_change:

            for edge in G.edges():

                resistance_change_file.write(f"{G.edges[edge]['resistance']}\t")

            resistance_change_file.write("\n")

        if conductances_change:

            for edge in G.edges():

                conductances_change_file.write(f"{G.edges[edge]['conductance']}\t")

            conductances_change_file.write("\n")
            
        if voltages_simple:
            voltages_simple_change_file.write(f"{voltages_simple[0]}\t")
            voltages_simple_change_file.write(f"{voltages_simple[1]}\n")

    return G





    