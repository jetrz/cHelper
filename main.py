from flask import request, flash, redirect, url_for
from flask_login import current_user
from website import create_app
from website.functions.misc.setUserAlgo import setUserAlgo

app = create_app()
app.app_context().push()

@app.route('/recurring-buy', methods=['POST', 'GET'])
def recurring_buy():
    """
    Recurring Buy algo settings page. Implements a simple recurring buy that increments the coin/stock balance for a user by a fixed quantity every given interval. 
    This implementation is currently done in main.py because of circular import issues using setUserAlgo.. if someone could fix this would be great :')
    
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
    coin = request.form.get('recurring_buy_coin')
    isOn = request.form.get('recurring_buy_isOn')
    interval = request.form.get('recurring_buy_interval')
    qty = request.form.get('recurring_buy_qty')
    
    if coin and isOn and interval and qty:
        isOn = bool(int(isOn))
        interval = float(interval)
        qty = float(qty)
        
        setUserAlgo(app, current_user.uid, 'recurringBuy', {'coin':coin, 'isOn':isOn, 'interval':interval, 'qty':qty})
        flash('Algo set!', category='success')
    else:
        flash('Please fill in all fields!', category='error')

    return redirect(url_for('views.recurring_buy'))
                

if __name__ == '__main__':
    app.run(debug=True, threaded=True)