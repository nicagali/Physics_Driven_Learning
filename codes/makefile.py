import matplotlib.pyplot as plt

# import training_memrisotrs
import graphs
import plotting_functions
import training
import networkx as nx

# VALTAGE DIVIDER AND MEMRISTOR

# G = graphs.simple_graph(save_data=True)

# G_trained = G.copy(as_view=False)
# # G_trained = training_memrisotrs.training_epoch(G_trained)
# G_trained = training.training_epoch(G_trained, rule='continuous', update='conductances')
# fig, ax = plt.subplots(3,1, figsize = (8.5,10))
# plotting_functions.simple_plot_voltages(ax[0], rule = 'continuous', update = 'conductances')
# plotting_functions.plot_conductaces_ratio(ax[1], G_trained)
# plotting_functions.plot_mse(ax[2], fig, rule = 'continuous', update = 'conductances', 
#                             zoom_in=0, scatter=True) 
# plt.savefig(f"{PLOT_PATH}Voltage_cond_mse.pdf")

# print("Final value conductances:", G_trained.edges[(0,1)]['conductance'], G_trained.edges[(1,2)]['conductance'])
# print("Final value conductances/initial:", G_trained.edges[(0,1)]['conductance']/initial_value_conductance, G_trained.edges[(1,2)]['conductance']/initial_value_conductance)
# print("Final value conductances-initial:",  G_trained.edges[(0,1)]['conductance'] - initial_value_conductance, G_trained.edges[(1,2)]['conductance']- initial_value_conductance)

# FIRST GENERAL GRAPH

# G = nx.read_graphml(f'{DATA_PATHG}graph1.graphml', node_type = int)

G = graphs.random_graph(save_data=True)
# G = nx.read_graphml(f'{DATA_PATHG}random_graph.graphml', node_type = int)
fig, ax = plt.subplots()
plotting_functions.plot_graph(ax, fig, 'random_graph')
plt.savefig("../notes/figures_tex/general_graph.pdf")

G1 = G.copy(as_view=False)
G2 = G.copy(as_view=False)

print("alpha=", alpha_r, "eta=", eta_r, "gamma=", gamma_r)

# ------ DISCRETE
G1 = training.training_epoch(G1, rule = 'discrete', update = 'resistances', mse=True, 
                             resistances_change=True)

fig, ax = plt.subplots(2,1, figsize = (12,10))
# plotting_functions.simple_plot_resistances(ax[0], rule = 'discrete')
plotting_functions.plot_resistances(ax[0], G1, rule = 'discrete')
plotting_functions.plot_mse(ax[1], fig, rule = 'discrete', update = 'resistances', zoom_in=0)
plt.savefig("../notes/figures_tex/general_training_random_disc.pdf")

# ------ CONTINUOUS
G2 = training.training_epoch(G2, rule = 'continuous', update = 'resistances', mse=True, 
                             resistances_change=True)

zoom = 0
fig, ax = plt.subplots(2,1, figsize = (12,10))
plotting_functions.plot_resistances(ax[0], G2, rule = 'continuous', zoom_in=zoom)
plotting_functions.plot_mse(ax[1], fig, rule = 'continuous', update = 'resistances', zoom_in=zoom)
plt.savefig("../notes/figures_tex/general_training_random_cont.pdf")