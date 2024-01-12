# PATHS

# Here insert the office path when you get back to the office

# PATH_TO_DIR = "/Users/monicaconte/PhD/Projects/Physics_Driven_Learning/"
PATH_TO_DIR = "/home/monicaconte/nica/phd/Projects/Dillavou/general_network/"
DATA_PATH = f"{PATH_TO_DIR}data/"
DATA_PATH_MEMR = f"{PATH_TO_DIR}data/memristors/"
PLOT_PATH = f"{PATH_TO_DIR}plots/"
DATA_PATHG = f"{PATH_TO_DIR}data/graphs/"
PLOT_PATHG = f"{PATH_TO_DIR}/plots/graphs/"

PATH_TO_DIR_ION = "/Users/monicaconte/PhD/Projects/Ionic_Channels/"
DATA_IONCHAN_PATH = f'{PATH_TO_DIR_ION}/data/'

# GRAPH PREFERENCES
numb_nodes = 9
numb_edges = 16
numb_source_nodes = 3
numb_target_nodes = 3
numb_hidden_nodes = numb_nodes - numb_target_nodes - numb_source_nodes

# TRAINING PARAMETERS
source_voltages = [5, 1, 1]
desired_output  = [3, 3, 3]
# desired_output = [4]

initial_value_resistances = 50
eta_r = 0.5
alpha_r = 5000
gamma_r = alpha_r/(2*eta_r)
delta_R = 0.781
# gamma_r = 500
tol = 1e-16

# initial_value_conductance = (1/50)*10**(-11)
initial_value_conductance = 1/50
initial_value_conductance = 4
# initial_value_conductance = 4e-12
eta_c = 0.5
# eta_c=1e-3
alpha_c = 0.003
# gamma_c = (alpha_c/eta_c)*10**(-11)
gamma_c = (alpha_c/(2*eta_c))
# gamma_c = 1e-14
# gamma_c = 0.001
delta_g = 0.0005

standard_dev = 0.01

iterations = 500

# time_interval = 

# PLOT PREFERENCES

# size
axis_fontsize = 17
legend_size = 15
size_ticks = 13
size_labels = 17

# colors
color_dots = ['firebrick','mediumorchid','silver']

# dictionaries

mse_discrete_style = dict(c = 'hotpink', lw=2, label = rf'Discrete rule')
mse_continuous_res_style = dict(c = 'darkmagenta', lw=2, label = rf'Continuous rule')

mse_continuous_res_style_1 = dict(c = 'tomato', lw=2, label = rf'$\eta = 1$')
mse_continuous_res_style_05 = dict(c = 'darkmagenta', lw=2, label = rf'$\eta = 0.5$')
mse_continuous_res_style_01 = dict(c = 'palevioletred', lw=2, label = rf'$\eta = 0.2$')

mse_continuous_res_style_scatter = dict(c = 'navy', marker='d', label = rf'continuous $R$, $\gamma_R =$ {gamma_r:.0f}')
mse_continuous_con_style = dict(c = 'skyblue', lw=3, label = rf'Continuous rule')
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