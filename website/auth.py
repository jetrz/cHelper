from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Wallet, recurringBuySettings
from.coins import COINS
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    #request.form is the data that was sent when this route was accessed
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #remembers that user is logged in until user logs out/server is refreshed etc.. 
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email is not valid!', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #this route can only be used if user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already in use!', category='error')
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
        else:
            #add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            
            #add wallet associated to user
            new_wallet = Wallet(uid=new_user.uid)
            db.session.add(new_wallet)
            db.session.commit()
            
            #add settings entry for all algos associated to user
            for i in range(len(COINS)):
                new_recurringBuySettings = recurringBuySettings(coin=COINS[i], uid=new_user.uid)
                db.session.add(new_recurringBuySettings)
            db.session.commit()
            
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
             
        
    return render_template("sign_up.html", user=current_user)