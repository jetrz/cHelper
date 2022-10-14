import threading
from time import sleep

from ..algos.recurringBuy import recurringBuy, exit, threadDone
from ... import db
from ...models import recurringBuySettings


def setUserAlgo(app, uid, algo, settings):
    """
    Updates settings for a users' algo.
    
    @params app: The current application.
    @params uid: Current users' UID.
    @params algo: The algo to update.
    @params settings: Dict of updated algo settings.
    @returns: Does not return anything.
    """
    
    # For recurring buy.
    if algo == 'recurringBuy':
        coin = settings['coin']
        isOn = settings['isOn']
        interval = settings['interval']
        qty = settings['qty']
        
        setting = recurringBuySettings.query.filter_by(uid=uid, coin=coin).first()
        if (setting is None):
            raise Exception("in setUserAlgo: recurringBuy, tuple for user's settings does not exist")
            
        # Update settings
        setting.isOn = isOn
        setting.interval = interval
        setting.qty = qty
        
        # If the user turned the algo off, kill the old thread if there is one. 
        if not isOn:
            if setting.hasThread:
                exit.set() # calls the semaphore from the old thread, killing it
                setting.hasThread = False
            db.session.commit()
            return
        
        # If the user turned the algo on, kill the old thread if there is one.
        if setting.hasThread:
            exit.set() # calls the semaphore from the old thread, killing it
            while not threadDone.is_set(): # wait for the old thread to exit
                sleep(1)
        else:
            setting.hasThread = True
        
        # Run the new thread.       
        exit.clear() 
        recurringBuyThread = threading.Thread(target=recurringBuy, args=(app, uid, interval, coin, qty))
        recurringBuyThread.start()
            
        db.session.commit()
        
        
        