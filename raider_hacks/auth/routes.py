from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint, render_template
from passlib.hash import sha256_crypt
from sqlalchemy import or_
from flask_login import login_user, logout_user, login_required, current_user

from raider_hacks import app, db, mail, Message
from raider_hacks.models import User, Post

import nacl.encoding

import nacl.hash


auth_bp = Blueprint('auth', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('auth/register.html')

    else:
        # Create user object to insert into SQL
        passwd1 = request.form.get('password1')
        passwd2 = request.form.get('password2')

        # Checks if passwords match
        if passwd1 != passwd2 or passwd1 == None:
            flash('Password Error!', 'danger')
            return render_template('auth/register.html')

#        hashed_pass = sha256_crypt.encrypt(str(passwd1))
        hashed_pass = nacl.hash.blake2b(passwd2,digest_size=64,encoder=nacl.encoding.URLSafeBase64Encoder)
        
        # Calls the User object from flask_app.models
        new_user = User(
            # username=request.form.get('username'),
            first_name=request.form.get('fname'),
            last_name=request.form.get('lname'),
            email=request.form.get('email'),
            password=hashed_pass,
            permissions=1)
        # removed new_user.username 
        if user_exists(new_user.email):
            flash('User already exsists!', 'danger')
            return render_template('auth/register.html')
        else:
            recipients = ['notjoemartinez@protonmail.com']
            for email in recipients:
                msg = Message('Flask-Mail Test', sender = 'raiderHacksMail@gmail.com', recipients = [email])
                msg.body = "{} {} would like to make an account on raiderHacks.com using {}".format(new_user.first_name, new_user.last_name, new_user.email)
                mail.send(msg)

            # Insert new user into SQL
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            flash('Account created!', 'success')
            return redirect(url_for('index'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    else:
        # username = request.form.get('username')
        email = request.form.get('email')
        password_candidate = request.form.get('password')

        # Query for a user with the provided email 
        result = User.query.filter_by(email=email).first()

        # If a user exsists and passwords match - login
        if result is not None and sha256_crypt.verify(password_candidate, result.password):

            # Init session vars
            login_user(result)
            flash('Logged in!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Incorrect Login!', 'danger')
            return render_template('auth/login.html')

########## 

@auth_bp.route("/logout")
def logout():
    logout_user()
    flash('Logged out!', 'success')
    return redirect(url_for('index'))


# Check if username or email are already taken
def user_exists(email):
    # Get all Users in SQL
    users = User.query.all()
    for user in users:
        if email == user.email:
            return True

    # No matching user
    return False
