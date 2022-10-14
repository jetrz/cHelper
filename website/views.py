from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
import json
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import threading

from . import db
from .coins import COINS
from .functions.misc.addValue import addValue
from .functions.misc.getPrices import getPrices
from .functions.optimisation.SETO import SETO
from .models import User, Wallet, histValues, recurringBuySettings

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    """
    Home/dashboard page. 
    Has the following features:
        - Balance information of users' wallet
        - Pie chart breakdown of users' wallet
        - Live data of BTC historical prices (WIP)
        - Section to allow user to update his wallet balance

    Main data structures used in this page:
    wallet_dict stores the users' balance for the various coins/stocks.
    wallet_dict = {
        'coin1': 1.0,
        'coin2': 2.0, 
        ...
    }
    
    prices_dict stores the latest prices for all the various coins/stocks.
    prices_dict = {
        'coin1': 3.14159,
        'coin2': 4.14159, 
        ...
    }
    """   
    
    print("Number of active threads:", threading.active_count())
    
    # If POST req was made to home page, update with latest current wallet values
    if request.method == 'POST':
        coin = request.form.get('update_wallet_coin')
        val = request.form.get('update_wallet_value')
        
        if coin and val:
            addValue(current_user.uid, coin, val)
        else:
            flash('Please fill in all fields!', category='error')
        
        return redirect(url_for('views.home'))
    
    # Retrieve users current wallet from DB
    current_wallet = Wallet.query.filter_by(uid=current_user.uid).first()

    # Convert coins in user's wallet to dictionary form, i.e. {'BTC':1.0, 'ETH':0.5}
    wallet_dict = dict((col, getattr(current_wallet, col)) for col in current_wallet.__table__.columns.keys())
    del wallet_dict['uid']
    
    # Get prices of all coins
    coins = []
    prices_dict = {}
    for coin in wallet_dict.keys():
            coins.append(coin)
    prices_dict = getPrices(coins)
    
    # Creation of wallet breakdown pie chart
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
        
    # Creation of historical coin values graph
    df_coin_hist_values = pd.read_sql(histValues.query.statement, db.engine)
    
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

@views.route('/recurring-buy', methods=['GET'])
@login_required
def recurring_buy():
    """
    Recurring Buy page for 'GET'. Just displays the users' current settings. 
    To see implementation of recurring buy, 'POST' page is in main.py.
    
    Implements a simple recurring buy that increments the coin/stock balance for a user by a fixed quantity every given interval.

    Main data structures used in this page:
    settings_dict stores the users' recurring buy algo settings for the various coins/stocks.
    settings_dict = {
        'coin1': {
            'isOn': False, 
            'interval': 0, 
            'qty': 0, 
            'coin': 'coin1'
        }, 
        ...
    }
    """      
    settings = recurringBuySettings.query.filter_by(uid=current_user.uid)
    settings_dict = {}
    for curr in settings:
        settings_dict[curr.coin] = {
            'isOn': curr.isOn,
            'interval': curr.interval,
            'qty': curr.qty,
            'coin': curr.coin        
        }
    
    return render_template("recurring_buy.html", user=current_user, settings_dict=settings_dict)

@views.route('/optimiser', methods=['GET', 'POST'])
@login_required
def optimiser():
    """
    Optimiser page. Implements the SETO algorithm as outlined in https://www.researchgate.net/figure/Flowchart-of-the-proposed-SETO-algorithm_fig3_352746389

    Main data structures used in this page:
    vals stores the information for the various coins/stocks.
    vals = {
        'coin1' : {
            'vars' : [[x0, y0], [x1, y1], ...] 2D array tracking historical values of the coin's variables.
            'fitness' : [fitness0, fitness1, ...] 1D array tracking historical values of the coin's fitness.
            'RSI' : [RSI0, RSI1, ...] 1D array tracking historical values of the coin's RSI. First k values will be 0, where k is the RSI timeframe.
            'nBuyers' : [nb1, nb2, ...] 1D array tracking historical values of the number of buyers in the queue for this coin.
            'nSellers' : [ns1, ns2, ...] 1D array tracking historical values of the number of sellers in the queue for this coin.
        },
        ...
    }
    """
    if request.method == 'POST':    
        # Submitted variables
        nTotalTraders = request.form.get('nTotalTraders')
        nIterations = request.form.get('nIterations')
        rsiTimeframe = request.form.get('rsiTimeframe')
        
        if nTotalTraders and nIterations and rsiTimeframe:
            nTotalTraders, nIterations, rsiTimeframe = int(nTotalTraders), int(nIterations), int(rsiTimeframe)
            vals = SETO(nTotalTraders, nIterations, rsiTimeframe)
            
            # Creation of display graphs
            dictVals = {
                'iter': [], 
                'coins': [],
                'nBuyers': [],
                'nSellers': [],
                'nTraders': [], 
                'fitness': [],
                'RSI': [],
                'x': [],
                'y': []
                }
            
            for coin in COINS:
                dictVals['iter'] += [i for i in range(nIterations+1)]
                dictVals['coins'] += [coin]*(nIterations+1)
                dictVals['nBuyers'] += vals[coin]['nBuyers']
                dictVals['nSellers'] += vals[coin]['nSellers']
                nb, ns = np.array(vals[coin]['nBuyers']), np.array(vals[coin]['nSellers'])
                nTraders = nb+ns
                dictVals['nTraders'] += nTraders.tolist()
                dictVals['fitness'] += vals[coin]['fitness']
                dictVals['RSI'] += vals[coin]['RSI']
                dictVals['x'] += [vals[coin]['vars'][i][0] for i in range(nIterations+1)]
                dictVals['y'] += [vals[coin]['vars'][i][1] for i in range(nIterations+1)]
            
            # for key, vals in dictVals.items():
                # print('key: ', key, 'len(vals): ', len(vals))
                
            df = pd.DataFrame(dictVals)
            figFitness = px.line(df, x='iter', y='fitness', color='coins')
            figTraders = px.line(df, x='iter', y=['nBuyers', 'nSellers', 'nTraders'], color='coins')
            figRSI = px.line(df, x='iter', y='RSI', color='coins')
            figVars = px.line(df, x='iter', y=['x', 'y'], color='coins') 
            graphFitnessJSON = json.dumps(figFitness, cls=plotly.utils.PlotlyJSONEncoder)  
            graphTradersJSON = json.dumps(figTraders, cls=plotly.utils.PlotlyJSONEncoder)  
            graphRSIJSON = json.dumps(figRSI, cls=plotly.utils.PlotlyJSONEncoder)
            graphVarsJSON = json.dumps(figVars, cls=plotly.utils.PlotlyJSONEncoder)    
            
            flash('Optimised!', category='error')    
            return render_template("optimiser.html", 
                                user=current_user,
                                graphFitnessJSON=graphFitnessJSON,
                                graphTradersJSON=graphTradersJSON,
                                graphRSIJSON=graphRSIJSON,
                                graphVarsJSON=graphVarsJSON,
                                )
        else:
            flash('Please fill in all fields!', category='error')
    
    return render_template("optimiser.html", user=current_user)   