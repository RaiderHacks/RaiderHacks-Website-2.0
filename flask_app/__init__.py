from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)

app.config['SECRET_KEY'] = '1A37BbcCJh67'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config
db = SQLAlchemy(app)


## login manager stuff
login_manager = LoginManager()
login_manager.init_app(app) # this inti_app

from flask_app import routes
