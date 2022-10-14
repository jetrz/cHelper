from .fitness import fitness
from .rising import rising
from .falling import falling 
from .calculateRSI import calcRSI
from ...coins import COINS

import heapdict
import math
import random

def SETO(nTotalTraders, nIterations, rsiTimeframe):
    """
    Optimiser page. Implements the SETO algorithm as outlined in https://www.researchgate.net/figure/Flowchart-of-the-proposed-SETO-algorithm_fig3_352746389

    Main data structures used in this page:
    vals stores the information for the various coins/stocks.
    vals = {
        'coin1' : {
            'vars' : [[x0, y0], [x1, y1], ...] 2D array tracking historical values of the coin's variables.
            'fitness' : [fitness0, fitness1, ...] 1D array tracking historical values of the coin's fitness.
            'RSI' : [RSI0, RSI1, ...] 1D array tracking historical values of the coin's RSI. First k values will be 0, where k is the RSI timeframe.
            'nBuyers' : [nb1, nb2, ...] 1D array tracking historical values of the number of buyers in the queue for this coin.
            'nSellers' : [ns1, ns2, ...] 1D array tracking historical values of the number of sellers in the queue for this coin.
        },
        ...
    }
    
    @param nTotalTraders: Number of total traders to simulate.
    @param nIterations: Number of iterations to run.
    @param rsiTimeframe: Timeframe (in days) for calculation of RSI.
    @returns vals: Information collected across the simulation.
    """
    
    # Setting the lower and upper bounds for the variables. 
    bounds = {
        0 : {
            'upper': 2,
            'lower': -1
        },
        1 : {
            'upper': 2,
            'lower': -1
        }
    }
    
    # Creation of initial population according to 3.2.1        
    vals = {}
    # Use a max/min heap to keep track of min & max fitness values and their respective coins.
    fitnessMaxHeap, fitnessMinHeap = heapdict.heapdict(), heapdict.heapdict()
    
    for coin in COINS:
        
        # Initializing vars & RSI
        curr = vals[coin] = {}
        curr['vars'] = [[(bounds[i]['upper']-bounds[i]['lower'])*random.random() + bounds[i]['lower'] for i in range(len(bounds))]]
        curr['RSI'] = [0]
        
        # Initializing fitness
        initCurrFitness = fitness(curr)
        curr['fitness'] = [initCurrFitness]
        fitnessMaxHeap[coin] = -1*initCurrFitness
        fitnessMinHeap[coin] = initCurrFitness
    
    # Initializing nBuyers and nSellers
    overallMinFitness = fitnessMinHeap.peekitem()[1]        
    sumOfFitnessDiff = sum(coininfo['fitness'][0]-overallMinFitness for coininfo in vals.values())
    for coin in COINS:
        curr = vals[coin]
        nf = (curr['fitness'][0]-overallMinFitness)/sumOfFitnessDiff   
        
        nTraders = round(nf*nTotalTraders)
        nBuyers = round(nTraders*random.random())
        nSellers = nTraders-nBuyers
        curr['nBuyers'] = [nBuyers]
        curr['nSellers'] = [nSellers]
        
    # Running of SETO algo. See psuedocode on page 18
    currIter = 0   
    while currIter < nIterations:
                    
        for coin in COINS:
            # print('curr coin: ', coin)
            curr = vals[coin]
            
            # Rising and falling phase
            if (currIter > rsiTimeframe and curr['RSI'][-1] <= 30):
                curr = rising(curr, bounds)
            elif (currIter > rsiTimeframe and curr['RSI'][-1] >= 70):
                curr = falling(curr, bounds)
            else:
                r = random.random()
                if r > 0.5:
                    curr = rising(curr, bounds)
                else:
                    curr = falling(curr, bounds)
                    
            # Calculate and update fitness of coin.
            # Update current fitness in vals, as well as in the fitness min and max heaps.
            currFitness = fitness(curr)
            curr['fitness'].append(currFitness)
            fitnessMaxHeap[coin] = -1*currFitness
            fitnessMinHeap[coin] = currFitness
                    
            # Exchange phase        
            # The algo changes the number of sellers and buyers by 1. Here, I change by 1%.
            if vals[fitnessMinHeap.peekitem()[0]]['nSellers'][-1] > 0:
                nTradersSwapped = math.ceil(vals[fitnessMinHeap.peekitem()[0]]['nSellers'][-1]*0.01)
                vals[fitnessMinHeap.peekitem()[0]]['nSellers'][-1] -= nTradersSwapped
                vals[fitnessMaxHeap.peekitem()[0]]['nBuyers'][-1] += nTradersSwapped
            
            # Calculate and update RSI.
            if (currIter >= rsiTimeframe):
                curr['RSI'].append(calcRSI(curr, rsiTimeframe))
            else:
                curr['RSI'].append(0)
        
        # Update the historical values of nBuyers and nSellers.
        for coin in COINS:
            vals[coin]['nBuyers'].append(vals[coin]['nBuyers'][-1])
            vals[coin]['nSellers'].append(vals[coin]['nSellers'][-1])
            
        currIter += 1
        
    return vals