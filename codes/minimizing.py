from scipy.optimize import minimize
from matplotlib.ticker import FuncFormatter
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from parameters import *

#  Minimize a simple function

def objective_function(x):
    return x**2 

initial_guess = 2.0

result = minimize(objective_function, initial_guess)

minimum_value = result.fun
minimum_location = result.x

x = np.linspace(-3,3,100)
plt.plot(x, objective_function(x))
plt.scatter(minimum_location, minimum_value, color='red')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.savefig("easy_minimum.pdf")

print(f"The minimum value is {minimum_value} at x = {minimum_location}")


def objective_function_bug(x, conductances):

    power = 0

    power += conductances[0] * (x[0] - x[1])**2
    power += conductances[1] * (x[1] - x[2])**2

    return power

def minimize_bug_fixing():

    initial_guess = [5,0,0]

    conductances = [initial_value_conductance, initial_value_conductance]
    
    cons = ({'type' : "eq", 'fun': lambda x: x[0]-5}, {'type' : "eq", 'fun': lambda x: x[2]-0})

    result = minimize(objective_function_bug, initial_guess, args=(conductances, ), constraints=cons, tol=1e-8)

    return result

result_minimization = minimize_bug_fixing()

print(result_minimization)
