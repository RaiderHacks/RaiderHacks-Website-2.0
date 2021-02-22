from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from flaskext.markdown import Markdown
import os, random 

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mXtMpIWMxnRdW0Fr'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465 # is this port open on deployment?
app.config['MAIL_USERNAME'] = 'raiderHacksMail@gmail.com'
app.config['MAIL_PASSWORD'] = 'BqV7VMFpg8vo5ZaGXxJqxQKBenhpDypWjeQ2uQPZDwzb3CQstTHH8JE5Ry'
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

db = SQLAlchemy(app)
# initalize markdown
md = Markdown(app)
## login manager stuff
login_manager = LoginManager()
login_manager.init_app(app) # this inti_app

from raider_hacks import main 

from raider_hacks.auth.routes import auth_bp
from raider_hacks.blog.routes import blog_bp 
from raider_hacks.posts.routes import post_bp
from raider_hacks.settings.routes import settings_bp

from raider_hacks.members.routes import members_bp
app.register_blueprint(members_bp)

app.register_blueprint(blog_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)
app.register_blueprint(settings_bp)



