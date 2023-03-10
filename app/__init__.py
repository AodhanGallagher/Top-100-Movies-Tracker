# Importing relevant modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager
import logging

# Initialising the application
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db, render_as_batch=True)

admin = Admin(app,template_mode='bootstrap4')

#Initialising the login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(userId):
    return User.query.get(int(userId))

# Specifying the file for the logs to be written to
logging.basicConfig(filename='TopMovies.log', filemode='w', level=logging.DEBUG)

from app import views, models