from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message


app = Flask(__name__)

app.config['SECRET_KEY'] = '1A37BbcCJh67'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'raiderHacksMail@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

db = SQLAlchemy(app)


## login manager stuff
login_manager = LoginManager()
login_manager.init_app(app) # this inti_app

from flask_app import routes
