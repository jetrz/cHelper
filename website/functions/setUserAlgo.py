import threading
from time import sleep

from ..models import User, recurringBuySettings
from .algos.recurringBuy import recurringBuy
from .. import db
from .algos.recurringBuy import exit, threadDone

def setUserAlgo(app, uid, algo, settings):
    # for recurring buy
    if algo == 'recurringBuy':
        coin = settings['coin']
        isOn = settings['isOn']
        interval = settings['interval']
        qty = settings['qty']
        
        setting = recurringBuySettings.query.filter_by(uid=uid, coin=coin).first()
        if (setting is None):
            raise Exception("in setUserAlgo: recurringBuy, tuple for user's settings does not exist")
            
        # update settings
        setting.isOn = isOn
        setting.interval = interval
        setting.qty = qty
        
        # user turned the algo off. 
        if not isOn:
            if setting.hasThread:
                exit.set() #kill the old thread
                setting.hasThread = False
            db.session.commit()
            return
        
        # user turned the algo on.
        if setting.hasThread: #if there is already an recurring buy thread running
            exit.set() #kill the old thread
            while not threadDone.is_set():
                sleep(1)
        else:
            setting.hasThread = True
        
        # run        
        exit.clear() 
        recurringBuyThread = threading.Thread(target=recurringBuy, args=(app, uid, interval, coin, qty))
        recurringBuyThread.start()
            
        db.session.commit()
        
        
        