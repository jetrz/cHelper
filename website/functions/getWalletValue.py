from .getPrices import getPrices

def getWalletValue(wallet_dict):
    #get prices of coins
    coins = []
    prices_dict = {}
    for coin, value in wallet_dict.items():
        coins.append(coin)
    prices_dict = getPrices(coins)
    
    currentWalletVal = 0
    for coin, value in prices_dict.items():
        currentWalletVal += value*wallet_dict[coin]
    
    return currentWalletVal