from datetime import datetime
from raider_hacks import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 1 user submitted application
# 2 user manually acceptaed 
# 3 user is an admin 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    # hmac = db.Column(db.String(128), unique=True, nullable=False)
    permissions = db.Column(db.Integer(), nullable=False, default=1)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return(self.email + ',' + str(self.permissions))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(120), nullable=False)
    permissions = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(self.id + ',' + str(self.permissions))

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    fname = db.Column(db.String(120), nullable=True)
    lname = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    profile_pic = db.Column(db.String(120), nullable=True)
    #    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    def __repr__(self):
        return "{},{},{},{},{}".format(self.fname, self.lname, self.email, self.bio, self.profile_pic)
 




