from ..addValue import addValue
from threading import Event

exit = Event()
threadDone = Event()

#recurringly update a users wallet at given time interval
def recurringBuy(app, uid, interval, coin, qty):
    threadDone.clear()
    with app.app_context():
       
        while not exit.is_set():            
            # add value into wallet
            addValue(uid, coin, qty)
                
            #interval is in days    
            exit.wait(interval*24*60*60)
    
    threadDone.set()
        
        