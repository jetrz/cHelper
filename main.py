from website import create_app
from flask import request, flash, redirect, url_for
from flask_login import current_user
from website.functions.setUserAlgo import setUserAlgo

app = create_app()
app.app_context().push()

@app.route('/recurring-buy', methods=['POST'])
def recurring_buy():
    coin = request.form.get('recurring_buy_coin')
    isOn = bool(int(request.form.get('recurring_buy_isOn')))
    interval = float(request.form.get('recurring_buy_interval'))
    qty = float(request.form.get('recurring_buy_qty'))
    setUserAlgo(app, current_user.uid, 'recurringBuy', {'coin':coin, 'isOn':isOn, 'interval':interval, 'qty':qty})
    flash('Algo set!', category='success')
    return redirect(url_for('views.recurring_buy'))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)