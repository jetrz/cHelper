from ..models import Wallet
from .. import db

def addValue(uid, coin, val):
    current_wallet = Wallet.query.filter_by(uid=uid).first()

    # if u can find a better way to do this that would be great. 
    # current_wallet.coin += val doesnt work because coin is a variable and u cant convert it to raw string in this call
    for key, value in current_wallet.__dict__.items():
        if key == coin:
            setattr(current_wallet, key, value+float(val))
    
    db.session.commit()