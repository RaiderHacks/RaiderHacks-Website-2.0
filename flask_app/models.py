from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 1 user submitted application
# 2 user manually acceptaed 
# 3 user is an admin 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    permissions = db.Column(db.Integer(), nullable=False, default=1)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return(self.id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(self.id)

class Addachievements(db.model):
    achievementID= db.Column(db.Integer, primary_key=True)
    postTitle= db.Column(db.String(120), nullable=False)
    postImage= db.Column(db.LargeBinary, nullable=False)
    content= db.Column(db.String(120), nullable=False)
    userID= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(self.id)

class Addmembers(db.model):
    membersID= db.Column(db.Integer, primary_key=True)
    postTitle= db.Column(db.String(120), nullable=False)
    postImage= db.Column(db.LargeBinary, nullable=False)
    content= db.Column(db.String(120), nullable=False)
    userID= db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(self.id)

