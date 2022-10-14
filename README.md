# Crypto Helper!

cHelper is a web application that allows users to test their own algorithms on real time crypto data. Made with Flask-SQLAlchemy.

### STRUCTURE:
- Run application from main.py.

- coins.py is for setting the coins available in this application
- models.py is for database schemas
- auth.py and views.py is for routing
- templates is the HTMLs, static\styles is the CSS
- functions->misc are the misc functions to help the application run.
- functions->algos are the algorithms to be implemented (i.e. recurring buy, stop-loss etc.)
- functions->optimisation is the implementation of SETO optimisation algo.

### TO BE DONE:
- Make graphs live
- Add more algos
- Fix bugs
- Beautify UI

### BUGS:
- HistValues tracker is a bit wonky. Mayb something to do w number of threads being created?

### LINKS:
- Python website tutorial: https://www.youtube.com/watch?v=dam0GPOAvVI 
- Get Crypto Price Data from CoinMarketCap: https://www.youtube.com/watch?v=opFegHZ7pUU AND https://coinmarketcap.com/api/documentation/v1/#tag/cryptocurrency
- Live Graph in Flask: https://towardsdatascience.com/web-visualization-with-plotly-and-flask-3660abf9c946#:~:text=The%20Flask%20app%20does%20a,it%20can%20display%20the%20charts AND https://plotly.com/python/range-slider/
- SETO Optimiser algo: https://link.springer.com/article/10.1007/s11227-021-03943-w
