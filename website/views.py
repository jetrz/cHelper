from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import User, Wallet, histValues, recurringBuySettings
from . import db

from .functions.addValue import addValue
from .functions.getPrices import getPrices

import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

import threading

views = Blueprint('views', __name__)

# ******************************** HOME PAGE ********************************
@views.route('/', methods=['POST', 'GET'])
@login_required #can only access this page if user is logged in
def home():
    print("Number of active threads:", threading.active_count())
    #get users current wallet from db
    current_wallet = Wallet.query.filter_by(uid=current_user.uid).first()
    
    #if POST req was made to home page, update with latest current wallet values
    if request.method == 'POST':
        coin = request.form.get('update_wallet_coin')
        val = request.form.get('update_wallet_value')
        addValue(current_user.uid, coin, val)
        return redirect(url_for('views.home'))

    #convert coins in user's wallet to dictionary form, i.e. {'BTC':1.0, 'ETH':0.5}
    wallet_dict = dict((col, getattr(current_wallet, col)) for col in current_wallet.__table__.columns.keys())
    del wallet_dict['uid']
    
    #get prices of all coins
    coins = []
    prices_dict = {}
    for coin in wallet_dict.keys():
            coins.append(coin)
    prices_dict = getPrices(coins)
    
    ### FOR HOME WALLET BREAKDOWN PIE CHART ###
    converted_wallet_dict = {'coins':[], 'values':[]}
    for coin, qty in wallet_dict.items():
        if qty > 0:
            converted_wallet_dict['coins'].append(coin)
            converted_wallet_dict['values'].append(qty*prices_dict[coin])
        
    df_wallet_breakdown = pd.DataFrame(converted_wallet_dict)
    
    fig_wallet_breakdown = px.pie(df_wallet_breakdown, values='values', names='coins', height=300, width=300)
    fig_wallet_breakdown.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    fig_wallet_breakdown.update_layout(margin_b=0, margin_l=0, margin_r=0, margin_t=0)
    
    wallet_breakdown_graphJSON = json.dumps(fig_wallet_breakdown, cls=plotly.utils.PlotlyJSONEncoder)
        
    ### FOR HOME HISTORICAL COIN VALUES GRAPH ###
    df_coin_hist_values = pd.read_sql(histValues.query.statement, r'sqlite:///C:\Users\joshu\OneDrive\Documents\cHelper\website\database.db')
    
    # Create figure
    fig_coin_hist_values = go.Figure()

    fig_coin_hist_values.add_trace(
        go.Scatter(x=list(df_coin_hist_values.timestamp), y=list(df_coin_hist_values.BTC)))

    # Set title
    fig_coin_hist_values.update_layout(
        title_text="Time series with range slider and selectors"
    )

    # Add range slider
    fig_coin_hist_values.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1h",
                        step="hour",
                        stepmode="backward"),
                    dict(count=1,
                        label="1d",
                        step="day",
                        stepmode="backward"),
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    home_graphJSON = json.dumps(fig_coin_hist_values, cls=plotly.utils.PlotlyJSONEncoder)
        
    return render_template("home.html", 
                           user=current_user, 
                           wallet=current_wallet, 
                           wallet_dict=wallet_dict, 
                           prices_dict=prices_dict,
                           wallet_breakdown_graphJSON=wallet_breakdown_graphJSON,
                           home_graphJSON=home_graphJSON)


# ******************************** RECURRING BUY PAGE ********************************
@views.route('/recurring-buy', methods=['GET'])
@login_required #can only access this page if user is logged in
def recurring_buy():      
    settings = recurringBuySettings.query.filter_by(uid=current_user.uid)
    # settings_dict will be in the form of = {'BTC': {'isOn': False, 'interval': 0, 'qty': 0, 'coin': 'BTC'}, 'ETH': {'isOn': False, 'interval': 0, 'qty': 0, 'coin': 'ETH'}, 'DOGE': {'isOn': False, 'interval': 0, 'qty': 0, 'coin': 'DOGE'}}
    settings_dict = {}
    for curr in settings:
        
        settings_dict[curr.coin] = {
            'isOn': curr.isOn,
            'interval': curr.interval,
            'qty': curr.qty,
            'coin': curr.coin        
        }
    
    return render_template("recurring_buy.html", user=current_user, settings_dict=settings_dict)