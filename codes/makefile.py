import matplotlib.pyplot as plt
from parameters import *
import training_memrisotrs
import graphs
import plotting_functions
import training

G = graphs.simple_graph(save_data=True)

G_trained = G.copy(as_view=False)
G_trained = training_memrisotrs.training_epoch(G_trained)
# G_trained = training.training_epoch(G_trained, rule='continuous', update='conductances')
fig, ax = plt.subplots(3,1, figsize = (8.5,10))
plotting_functions.simple_plot_voltages(ax[0], rule = 'continuous', update = 'conductances')
plotting_functions.plot_conductaces_ratio(ax[1], G_trained)
plotting_functions.plot_mse(ax[2], fig, rule = 'continuous', update = 'conductances', 
                            zoom_in=0, scatter=True) 
plt.savefig(f"{PLOT_PATH}Voltage_cond_mse.pdf")

print("Final value conductances:", G_trained.edges[(0,1)]['conductance'], G_trained.edges[(1,2)]['conductance'])
print("Final value conductances/initial:", G_trained.edges[(0,1)]['conductance']/initial_value_conductance, G_trained.edges[(1,2)]['conductance']/initial_value_conductance)
print("Final value conductances-initial:",  G_trained.edges[(0,1)]['conductance'] - initial_value_conductance, G_trained.edges[(1,2)]['conductance']- initial_value_conductance)


