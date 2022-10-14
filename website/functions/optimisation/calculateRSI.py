def calcRSI(curr, k):
    """
    Calculates the RSI for a given coin/stock at a given iteration.
    See 3.2.5 for full details.
    
    @params curr: Current coin/stock to calculate RSI for.
    @params k: RSI timeframe
    @returns: Calculated RSI
    """
    p, n = 0, 0
    for i in range(-1, -k+1, -1):
        if curr['fitness'][i] == curr['fitness'][i-1]:
            continue
        elif curr['fitness'][i] - curr['fitness'][i-1] > 0:
            p += 1
        else:
            n += 1
    
    if n:
        rs = p/n
    else:
        rs = n    
    RSI = 100 - 100/(1+rs)
    return RSI