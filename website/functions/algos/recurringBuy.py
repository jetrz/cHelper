from ..misc.addValue import addValue
from threading import Event

# Creating sempahores to facilitate the running of this algo
exit = Event()
threadDone = Event()

def recurringBuy(app, uid, interval, coin, qty):
    """
    To be called using a thread to recurringly increment the balance of a coin in the user's wallet.
    
    @param app: The current application.
    @param uid: Current users' uid.
    @param interval: The amount of time (in days) to wait between each increment
    @param coin: The coin to be added.
    @param qty: The amount to be added each increment.
    @returns Does not return anything.
    """ 
    threadDone.clear()
    
    with app.app_context():
        while not exit.is_set():            
            addValue(uid, coin, qty)  
            exit.wait(interval*24*60*60)
    
    threadDone.set()
        
        