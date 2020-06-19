import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)


app.config['SECRET_KEY'] = '12e011ac4f3f3bf10ae250cb9a45ffb2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app)



login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from todo import routes