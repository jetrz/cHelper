import math
import random

def falling(curr, bounds):
    """
    Simulates the falling of the stock. Decreases variables and buyer/seller ratio.
    See 3.2.3 for full details.
    @param curr: Info of the current coin/stock to simulate. Has the format: 
      {
          'vars' : [[x0, y0], [x1, y1], ...] 2D array tracking historical values of the coin's variables.
          'fitness' : [fitness0, fitness1, ...] 1D array tracking historical values of the coin's fitness.
          'RSI' : [RSI0, RSI1, ...] 1D array tracking historical values of the coin's RSI. First k values will be 0, where k is the RSI timeframe.
          'nBuyers' : [nb1, nb2, ...] 1D array tracking historical values of the number of buyers in the queue for this coin.
          'nSellers' : [ns1, ns2, ...] 1D array tracking historical values of the number of sellers in the queue for this coin.
      }
    @param bounds: Bounds of the variables of the coin/stock. Has the format:
      {
          0 : {
              'upper' : upperLimitOfVariable0,
              'lower' : lowerLimitOfVariable0
          },
          ...
      }
    @returns curr: Updated info of the coin/stock to simulate.
    """
    
    nc = min(curr['nSellers'][-1]/(curr['nBuyers'][-1]+1), 2)
    # d is a normalised variable representing the difference in variables between the local best and the current value.
    # The implementation here is slightly different from that in the report, although it is still a normalised value.
    d = sum(abs(bounds[i]['lower']-curr['vars'][-1][i])/(bounds[i]['upper']-bounds[i]['lower']) for i in range(len(bounds)))/len(bounds) # using this as a temporary normalised value. diff from formula in docs
    
    # Calculate the decreased values.
    nextVars = []
    for i in range(len(bounds)):
        randMultipler = float(random.randint(0, round(nc*d*100))/100)
        
        # Adds an element of randomness to help escape local optimas.
        # This is not implemented in the algorithm in the report. 
        randMultipler += random.randint(0,10)/100
        
        # This implementation is slightly different from that in the report. 
        # However, maintains the idea that if the current value is already low, decremented value should be less.
        nextVars.append(curr['vars'][-1][i] - randMultipler*(curr['vars'][-1][i] - bounds[i]['lower']))    
    curr['vars'].append(nextVars)
    
    # Decrement buyers and increment sellers for this coin/stock.
    if curr['nBuyers'][-1] > 0:
        nTradersSwapped = math.ceil(curr['nBuyers'][-1]*0.01)
        curr['nBuyers'][-1] -= nTradersSwapped
        curr['nSellers'][-1] += nTradersSwapped
        
    return curr