# database models

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from .coins import COINS

# schema for user to be stored in database
class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True) #auto increment
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    
    def get_id(self):
        return self.uid
    
# schema for wallet, each wallet associated with one user
class Wallet(db.Model):
    #create a column for each coin
    for i in range(len(COINS)):
        vars()[f"{COINS[i]}"] = db.Column(db.Float, default=0)
        
    #set uid as primary key
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    
# schema for historical values of all coins. this table will be updated periodically
class histValues(db.Model):
    #create a column for each coin
    for i in range(len(COINS)):
        vars()[f"{COINS[i]}"] = db.Column(db.Float, default=0)    
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now(), primary_key=True)
    
# schema for algo settings for user for recurring buy, primary key is (coin, uid). each entry is for one coin
class recurringBuySettings(db.Model):
    isOn = db.Column(db.Boolean, default=False)
    hasThread = db.Column(db.Boolean, default=False)
    interval = db.Column(db.Float, default=0)
    qty = db.Column(db.Float, default=0)
    coin = db.Column(db.String(10), primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)

    