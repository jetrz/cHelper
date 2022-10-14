from .getPrices import getPrices

def getWalletValue(wallet_dict):
    """
    Gets the total value of the users' current wallet.
    
    @params wallet_dict: Users' current wallet. Has the format:
    wallet_dict = {
        'coin1': 1.0,
        'coin2': 2.0, 
        ...
    }
    """
    
    coins = []
    prices_dict = {}
    for coin, value in wallet_dict.items():
        coins.append(coin)
    prices_dict = getPrices(coins)
    
    currentWalletVal = 0
    for coin, value in prices_dict.items():
        currentWalletVal += value*wallet_dict[coin]
    
    return currentWalletVal