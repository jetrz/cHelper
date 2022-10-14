from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from .coins import COINS

# Database schemas.

# User profile information.
class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True) # Auto increment
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    
    def get_id(self):
        return self.uid
    
# User's wallet information. Each entry is one wallet, and each user only has one wallet and vice versa.
class Wallet(db.Model):
    # Create a column for each coin
    for i in range(len(COINS)):
        vars()[f"{COINS[i]}"] = db.Column(db.Float, default=0)
        
    # Set uid as primary key
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    
# Historical values of all coins for the live graph on dashboard. This table will be updated periodically.
class histValues(db.Model):
    #create a column for each coin
    for i in range(len(COINS)):
        vars()[f"{COINS[i]}"] = db.Column(db.Float, default=0)    
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now(), primary_key=True)
    
# Users' Recurring Buy algo settings. Each entry is for one coin for one user, i.e. primary key is (coin, uid).
class recurringBuySettings(db.Model):
    isOn = db.Column(db.Boolean, default=False)
    hasThread = db.Column(db.Boolean, default=False)
    interval = db.Column(db.Float, default=0)
    qty = db.Column(db.Float, default=0)
    coin = db.Column(db.String(10), primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)

    