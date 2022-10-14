import json
from requests import Request, Session

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

headers = {
    'Accepts':'application/json',
    'X-CMC_PRO_API_KEY':'c935f01e-f5d9-420e-8ac5-7957d831eb3e'
}

session = Session()
session.headers.update(headers)

def getPrices(coins):
    """
    Gets the prices for the various coins that this application currently supports.
    Currently retrieving from CoinMarketCap.
    
    @param coins: Array/list of coins to retrieve prices for.
    @returns Dict cointaining the prices for each coin. Has the format:
    prices_dict = {
        'coin1': 3.14159,
        'coin2': 4.14159, 
        ...
    }
    """ 
    
    # Fetching the slugs for the currently supported coins. Hardcoded in. Would be great if could find a way to automate this.
    slugs = ''
    for coin in coins:
        match coin:
            case "BTC":
                slugs += 'bitcoin,'
            case "ETH":
                slugs += 'ethereum,'
            case "DOGE":
                slugs += 'dogecoin,'
    slugs = slugs[:-1]
    
    parameters = {
        'slug': slugs,
        'convert':'SGD',
    }
    
    # GET request to CoinMarketCap
    response = json.loads(session.get(url, params=parameters).text)
    
    # Parse response and return.
    prices = {}
    for coin in coins:
        for coininfo in response['data'].values():
            if coininfo['symbol'] == coin:
                 prices[coin] = coininfo['quote']['SGD']['price']
        
    return prices
    