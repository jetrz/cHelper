from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

import threading

#database variables
db = SQLAlchemy()
DB_NAME = "database.db"

#initializing the app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'wow fantastic baby'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    #for routes
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    #for db
    from .models import User
    create_database(app)
        
    #where the login manager should redirect user to if they are not logged in
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader #use the below function to load the user
    def load_user(uid):
        return User.query.get(int(uid)) #search from user using primary key (uid)
    
    #starts thread to track historical data for coins
    from .functions.updateCoinHistValues import updateCoinHistValues
    x = threading.Thread(target=updateCoinHistValues, args=(app,))
    x.start()
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all(app=app)
