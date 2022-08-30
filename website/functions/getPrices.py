from requests import Request, Session
import json
import pprint

url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

headers = {
    'Accepts':'application/json',
    'X-CMC_PRO_API_KEY':'c935f01e-f5d9-420e-8ac5-7957d831eb3e'
}

session = Session()
session.headers.update(headers)

def getPrices(coins):
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
    
    response = json.loads(session.get(url, params=parameters).text)
    
    prices = {}
    for coin in coins:
        for coininfo in response['data'].values():
            if coininfo['symbol'] == coin:
                 prices[coin] = coininfo['quote']['SGD']['price']
        
    return prices
    