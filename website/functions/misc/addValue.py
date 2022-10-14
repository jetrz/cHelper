from ...models import Wallet
from ... import db

def addValue(uid, coin, val):
    """
    Adds the balance for a coin in the users' wallet.
    To subtract, input a negative number.
    
    @param uid: Current users' uid.
    @param coin: The coin to be added.
    @param val: The amount to be added.
    @returns Does not return anything.
    """ 
    current_wallet = Wallet.query.filter_by(uid=uid).first()

    # If can find a better way to do this that would be great. 
    # current_wallet.coin += val doesnt work because coin is a variable and you cant convert it to raw string in this call
    for key, value in current_wallet.__dict__.items():
        if key == coin:
            setattr(current_wallet, key, value+float(val))
    
    db.session.commit()