import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from parameters import *

def plot_graph(ax, fig, name_graph, save_plot=False):

    # Get data
    G = nx.read_graphml(f'{DATA_PATHG}{name_graph}.graphml')
    color_attributes = [G.nodes[node]['color'] for node in G.nodes()]
    # labels = {node: f'{node} V= {voltages[node]:.2f}' for node in G.nodes()}
    nx.draw(G, with_labels=True, node_color=color_attributes)
   
    if save_plot:
        fig.savefig(f"{PLOT_PATHG}{name_graph}.pdf")

def plot_mse(ax, fig, rule, update, zoom_in, save_plot=False, 
             average=False, new_rule=False, scatter=False):

    x = range(iterations)
    if new_rule==False:
        y = np.loadtxt(f"{DATA_PATH}mse_{rule}_{update}.txt", unpack=True)
    else:
        y = np.loadtxt(f"{DATA_PATH}mse_{rule}_{update}_newrule.txt", unpack=True)
        

    x = x[zoom_in:]
    y = y[zoom_in:]

    if average:
        average_value = 0
        for i in range(iterations):
            average_value += y[i] 
        average_value/=iterations

    if rule == 'discrete':
        ax.semilogy(x, y, **mse_discrete_style)
        if average:
            ax.axhline(y = average_value, **mse_discrete_style)
    if rule == 'continuous' and update == 'resistances':
        if scatter:
            ax.set_yscale('log')
            ax.scatter(x, y, **mse_continuous_res_style_scatter)
        else:
            ax.semilogy(x, y, **mse_continuous_res_style)
        if average:
            ax.axhline(y = average_value, **mse_continuous_res_style)
    if rule == 'continuous' and update == 'conductances' and new_rule==False:
        if scatter:
            ax.set_yscale('log')
            ax.scatter(x, y, **mse_continuous_con_style_scatter)
        else:
            ax.semilogy(x, y, **mse_continuous_con_style)
    if rule == 'continuous' and update == 'conductances' and new_rule:
        if scatter:
            ax.set_yscale('log')
            ax.scatter(x, y, **mse_continuous_con_style_scater_new)
        else:
            ax.semilogy(x, y, **mse_continuous_con_style_new)


    if save_plot:
        fig.savefig(f"{PLOT_PATH}mse_{rule}_{update}.pdf")

    ax.tick_params('y', labelsize=size_ticks)
    ax.tick_params('x', labelsize=size_ticks)
    ax.set_xlim(np.min(x), np.max(x))

    ax.legend(fontsize = legend_size)
    ax.set_ylabel(r'$C$', fontsize = axis_fontsize)
    ax.set_xlabel(r'steps', fontsize = axis_fontsize)

    ax.grid(ls=':')
    
def plot_resistances(ax, G, rule):

    numb_edges = G.number_of_edges()
    # x = range(iterations)

    resistance_data = np.genfromtxt(f"{DATA_PATH}resistances_change_{rule}.txt", unpack=True)

    # print(np.shape(resistance_data))

    # print(len(resistance_data))

    for edge in range(numb_edges):

        if numb_edges==1:
            y = resistance_data
            x = range(len(resistance_data))
        else:    
            res_values = resistance_data[edge]

            x = range(len(resistance_data[edge]))
            y = []
            for i in range(len(resistance_data[edge])):
                if res_values[i] != 'removed':
                    y.append(res_values[i])

        ax.plot(x, y, lw = 2)
    
    ax.grid(ls=':')

    ax.set_ylabel(r'$R(\Omega)$', fontsize = axis_fontsize)
    ax.tick_params('y', labelsize=size_ticks)
    ax.set_xticklabels([])
    ax.set_xlim(np.min(x), np.max(x))

def plot_conductaces(ax, G):

    numb_edges = G.number_of_edges()

    conductance_data = np.genfromtxt(f"{DATA_PATH}conductances_change.txt", unpack=True)

    print(conductance_data[0])

    for edge in range(len(conductance_data)):

        cond_values = conductance_data[edge]

        x = [0]
        x.extend(range(1,len(conductance_data[edge])+1))
        y = [initial_value_conductance]
        y.extend(cond_values)
        
        if edge==0:
            ax.plot(x, y, lw = 3, color = 'silver', label=r'$g_1$')
        else:
            ax.plot(x, y, lw = 3, color = 'dimgray', label=r'$g_2$')

    ax.legend(fontsize=legend_size)
    
    ax.grid(ls=':')

    ax.set_ylabel(r'$g$', fontsize = axis_fontsize)
    ax.tick_params('y', labelsize=size_ticks)
    # ax.set_xticklabels([])
    ax.set_xlim(np.min(x), np.max(x))

def plot_conductaces_ratio(ax, G):

    conductance_data = np.genfromtxt(f"{DATA_PATH}conductances_change.txt", unpack=True)

    for edge in range(len(conductance_data)):

        cond_values = conductance_data[edge]

        x = [0]
        x.extend(range(1,len(conductance_data[edge])+1))
        y = [initial_value_conductance]
        y.extend(cond_values)
        
        if edge==0:
            ax.plot(x, y, lw = 3, color = 'silver', label=r'$g_1$')
        else:
            ax.plot(x, y, lw = 3, color = 'dimgray', label=r'$g_2$')

    
    ax.grid(ls=':')

    ax.set_ylabel(r'$g$', fontsize = axis_fontsize)
    ax.tick_params('y', labelsize=size_ticks)
    # ax.set_xticklabels([])
    ax.set_xlim(np.min(x), np.max(x))   

    ax2 = ax.twinx()

    x = range(0,len(conductance_data[edge])+1)

    # y = [1, np.array(conductance_data[0])/np.array(conductance_data[1])]

    y = np.concatenate(([1], np.array(conductance_data[0])/np.array(conductance_data[1])))

    ax2.plot(x, y, lw = 3, color = 'cadetblue', label=r'$g_1/g_2$')

    ax2.plot(x, [4]*(len(x)), ls = ':', color = 'cadetblue', lw = 2.5)

    ax.legend(fontsize=legend_size)
    
    # ax2.legend(fontsize=legend_size)


def simple_plot_voltages(ax, rule, update):

    x = np.array(range(iterations))

    desired_voltage = np.loadtxt(f"{DATA_PATH}voltages_simple_change_{rule}_{update}.txt", unpack=True, max_rows = 1)
    voltage_data = np.loadtxt(f"{DATA_PATH}voltages_simple_change_{rule}_{update}.txt", unpack=True, skiprows = 1)

    voltage_free = voltage_data[0]
    voltage_clamped = voltage_data[1]
    voltage_desired = [desired_voltage for _ in range(iterations)]
    
    ax.plot(x,voltage_desired , **marker_style_volt[2])
    ax.plot(x,voltage_clamped , **marker_style_volt[1])
    ax.plot(x,voltage_free , **marker_style_volt[0])


    ax.set_xlim(np.min(x), np.max(x))
    # ax.set_xlabel("Training Steps", fontsize = axis_fontsize)
    ax.set_xticklabels([])
    # ax.tick_params('x', labelsize=size_ticks)

    ax.set_ylabel(r'$V^{O}(V)$', fontsize = axis_fontsize)
    ax.tick_params('y', labelsize=size_ticks)

    ax.grid(ls=':')
    ax.legend(fontsize = legend_size)

def difference_mse(ax):

    mse = np.loadtxt(f"{DATA_PATH}mse_continuous_conductances.txt", unpack=True)
    mse_newrule = np.loadtxt(f"{DATA_PATH}mse_continuous_conductances_newrule.txt", unpack=True)

    difference = mse - mse_newrule

    ax.set_yscale('log')
    x = range(len(mse))
    ax.scatter(x, difference, marker='X', color = 'turquoise', s = 100)

    ax.grid(ls=':')
    ax.set_ylabel(r'$C - C_{new}$', fontsize = axis_fontsize)
    ax.set_xlabel(r'steps', fontsize = axis_fontsize)

    ax.tick_params('y', labelsize=size_ticks)
    ax.tick_params('x', labelsize=size_ticks)
    ax.set_xlim(np.min(x), np.max(x))
    



