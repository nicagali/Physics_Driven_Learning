import numpy as np
import networkx as nx
import random
from parameters import *
import analysis
import training
import sys
sys.path.append('../../../Ionic_Channels/codes')
import odeint_solver

def update_conductances_memr(G_free, G_clamped, g_solution, type_update):

    G_out = training.update_conductances(G_free, G_clamped, rule='countinuous')

    if type_update=='memer_coupled':

        G_out.edges[0] = g_solution

    return G_out

def train_memr(G, g_solution):

    G_free = G.copy(as_view=False)
    G_free = training.minimize_graph(G_free, 'free')
    
    G_clamped = G.copy(as_view=False)
    G_clamped = training.update_clamped(G_clamped)

    G_clamped = training.minimize_graph(G_clamped, 'clamped')
    G = update_conductances_memr(G_free, G_clamped, g_solution, type_update = 'both_coupled')
        
    voltages_simple=[]
    voltages_simple = [G_free.nodes[1]['voltage'], G_clamped.nodes[1]['voltage']]

    return G, voltages_simple

def training_epoch(G):

    voltages_change_file = open(f"{DATA_PATH_MEMR}voltages_change.txt", "w") 
    voltages_change_file.write(f"{desired_output[0]}\n")

    conductances_change_file = open(f"{DATA_PATH}conductances_change.txt", "w") 

    odeint_solver.euler_forward_solver('square')
    data = np.loadtxt(f"{DATA_IONCHAN_PATH}solution_euler.txt", unpack=True)
    g_solution = data[1]

    for step in range(iterations):

        G, voltages = train_memr(G, g_solution[step])

        for edge in G.edges():

            conductances_change_file.write(f"{G.edges[edge]['conductance']}\t")

        conductances_change_file.write("\n")
            
        voltages_change_file.write(f"{voltages[0]}\t")
        voltages_change_file.write(f"{voltages[1]}\n")
