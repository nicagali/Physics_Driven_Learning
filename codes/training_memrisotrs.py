import numpy as np
import networkx as nx
import random
from parameters import *
import analysis
import training
import sys
sys.path.append('/home/monicaconte/nica/phd/Projects/Ionic_Channels/codes')
import odeint_solver
from parameters_channels import *

def update_conductances_memr(G_free, G_clamped, g_solution1, g_solution2, type_update):

    G_out = training.update_conductances(G_free, G_clamped, rule='countinuous')

    if type_update=='memr_coupled':

        G_out.edges[(0,1)]['conductance'] = g_solution1

    if type_update=='memr_both':

        G_out.edges[(0,1)]['conductance'] = g_solution1
        G_out.edges[(1,2)]['conductance'] = g_solution2

    return G_out

def train_memr(G, g_solution1, g_solution2):

    G_free = training.minimize_graph(G, 'free', update='conductances')

    G_free = G_free.copy(as_view=False)
    
    G_clamped = training.update_clamped(G, update='conductances')
    
    G_clamped = training.minimize_graph(G_clamped, 'clamped', update='conductances')

    G = update_conductances_memr(G_free, G_clamped, g_solution1, g_solution2, type_update = 'memr_both')
        
    voltages_simple=[]
    voltages_simple = [G_free.nodes[1]['voltage'], G_clamped.nodes[1]['voltage']]

    return G, voltages_simple

def training_epoch(G):

    print("Initial value conductance:", initial_value_conductance, "Gamma c:", gamma_c)

    voltages_change_file = open("/home/monicaconte/nica/phd/Projects/Dillavou/general_network/data/voltages_simple_change_continuous_conductances.txt", "w") 
    voltages_change_file.write(f"{desired_output[0]}\n")

    conductances_change_file = open("/home/monicaconte/nica/phd/Projects/Dillavou/general_network/data/conductances_change.txt", "w") 

    mse_file = open(f"/home/monicaconte/nica/phd/Projects/Dillavou/general_network/data/mse_continuous_conductances.txt", "w")

    odeint_solver.euler_forward_solver('square', conductance_numb='g1')
    data = np.loadtxt(f"/home/monicaconte/nica/phd/Projects/Ionic_Channels/data/solution_euler.txt", unpack=True)
    g_solution1 = data[1]
    odeint_solver.euler_forward_solver('square', conductance_numb='g2')
    data = np.loadtxt(f"/home/monicaconte/nica/phd/Projects/Ionic_Channels/data/solution_euler.txt", unpack=True)
    g_solution2 = data[1]


    for step in range(iterations):

        G, voltages = train_memr(G, g_solution1[step], g_solution2[step])
        # G, voltages = train_memr(G, 1)

        for edge in G.edges():

            conductances_change_file.write(f"{G.edges[edge]['conductance']}\t")

        conductances_change_file.write("\n")
            
        voltages_change_file.write(f"{voltages[0]}\t")
        voltages_change_file.write(f"{voltages[1]}\n")

        ms_error_value = analysis.ms_error(G)

        if step == 0:
                
            ms_normalization = ms_error_value
            
        mse_file.write(f"{ms_error_value/ms_normalization}\n")

    return G
