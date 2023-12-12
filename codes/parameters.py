# PATHS

DATA_PATH = '../../data/'
DATA_PATH_MEMR = '../../data/memristors'
PLOT_PATH = '../../plots/'
DATA_PATHG = '../../data/graphs/'
PLOT_PATHG = '../../plots/graphs/'
DATA_IONCHAN_PATH = '../../../Ionic_Channels/data/'

# GRAPH PREFERENCES
numb_nodes = 9
numb_edges = 16
numb_source_nodes = 3
numb_target_nodes = 3
numb_hidden_nodes = numb_nodes - numb_target_nodes - numb_source_nodes
s
# TRAINING PARAMETERS
source_voltages = [5, 1, 0]
# desired_output  = [3, 3, 3]
desired_output = [4]

initial_value_resistances = 50
eta_r = 0.5
alpha_r = 5e3
gamma_r = alpha_r/eta_r
delta_R = 0.781
# gamma_r = delta_R
tol = 1e-16

initial_value_conductance = 1/50
eta_c = 0.5
alpha_c = 5e-4
gamma_c = alpha_c/eta_c
delta_g = 0.0005

standard_dev = 0.01

iterations = 20

# PLOT PREFERENCES

# size
axis_fontsize = 17
legend_size = 15
size_ticks = 13

# colors
color_dots = ['firebrick','mediumorchid','silver']

# dictionaries

mse_discrete_style = dict(c = 'blueviolet', lw=2, label = 'discrete')
mse_continuous_res_style = dict(c = 'navy', lw=2, label = rf'continuous $R$, $\gamma_R =$ {gamma_r:.0f}')
mse_continuous_res_style_scatter = dict(c = 'navy', marker='d', label = rf'continuous $R$, $\gamma_R =$ {gamma_r:.0f}')
mse_continuous_con_style = dict(c = 'skyblue', lw=3, label = rf'continuous $g$, $\gamma_g =$ {gamma_c}')
mse_continuous_con_style_new = dict(c = 'olive', lw=2, label = rf'continuous $g$ new, $\gamma_g =$ {gamma_c}')
mse_continuous_con_style_scatter = dict(c = 'skyblue', marker="d", s=60, label = rf'continuous $g$, $\gamma_g =$ {gamma_c}')
mse_continuous_con_style_scater_new = dict(c = 'olive', marker='P', label = rf'continuous $g$ new, $\gamma_g =$ {gamma_c}')

marker_style_volt = []
marker_style = dict(ls='-', lw=2, c='blue', label='Free')
marker_style_volt.append(marker_style)
marker_style = dict(ls='-', lw=4, c='black', label='Clamped')
marker_style_volt.append(marker_style)
marker_style= dict(ls='--', lw=2, c='gray', label='Desired')
marker_style_volt.append(marker_style)