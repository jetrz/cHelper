from .getPrices import getPrices
from ..models import histValues
from .. import db
from ..coins import COINS

from datetime import datetime
import time 
import threading
import logging

#to be run upon app init. tracks historical prices of coins in DB.
def updateCoinHistValues(app):
    with app.app_context():   
    
        while (True):
            prices_dict = getPrices(COINS)
            
            histEntry = histValues(**prices_dict)  
            #histEntry = histValues(BTC=prices_dict["BTC"],ETH=prices_dict["ETH"],DOGE=prices_dict["DOGE"],timestamp=datetime.now())
            db.session.add(histEntry)
            db.session.commit()
            logging.debug(datetime.now())
            logging.debug(threading.get_ident())
            logging.debug(threading.active_count())            
            time.sleep(60)
        