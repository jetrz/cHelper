from .getPrices import getPrices
from ...models import histValues
from ... import db
from ...coins import COINS

import time 

def updateCoinHistValues(app):
    """
    To be run upon app init. Periodically inserts an entry of coin prices in DB.
    
    @params app: The current application.
    """
    
    with app.app_context():   
    
        while (True):
            prices_dict = getPrices(COINS)
            
            histEntry = histValues(**prices_dict)  
            db.session.add(histEntry)
            db.session.commit()
                   
            time.sleep(60)
        