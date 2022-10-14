import math

def fitness(curr):
    """
    Objective function for optimisation.
    Currently using Peak Function.
    
    @params curr: Current coin/stock to calculate fitness for.
    @returns: Calculated fitness.
    """
    
    x = curr['vars'][-1][0]
    y = curr['vars'][-1][1]
    # res = math.cos(x)*math.sin(y) - x/(pow(y,2) + 1) Adjiman's. Not used now
    res = x*math.exp(-1*(pow(x,2)+pow(y,2)))
    
    return res