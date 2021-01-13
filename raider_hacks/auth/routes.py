from flask import Flask,render_template, request, redirect, url_for, flash
from flask import Blueprint, render_template
from passlib.hash import sha256_crypt
from sqlalchemy import or_
from flask_login import login_user, logout_user, login_required, current_user

from raider_hacks import app, db, mail, Message
from raider_hacks.models import User, Post

import nacl.encoding

import nacl.hash

import nacl.utils

import base64

from zxcvbn import zxcvbn


auth_bp = Blueprint('auth', __name__,
    template_folder='templates',
    static_folder='static'
)

@auth_bp.route("/gpg")
def gpg():
        return render_template('auth/gpg.html')

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('auth/register.html')

    else:
        
        if request.form.get('first-name') != None or request.form.get('last-name') != None or request.form.get('email-address') != None or request.form.get('password_1') != None or request.form.get('password_2') != None:
            print("Honeypot found")
            print(request.form.get('last-name'))
            return render_template('auth/register.html'),401

        if request.form.get('fname') == None or request.form.get('fname') == "" or request.form.get('lname') == None or request.form.get('lname') == "" or request.form.get('email') == None or request.form.get('email') == "" or request.form.get('password1') == None or request.form.get('password1') == "" or request.form.get('password2') == None or request.form.get('password2') == "":
            print("At least one field empty!")
            return render_template('auth/register.html'),401

        print("Last Name: " + request.form.get('lname'))

        # Create user object to insert into SQL
        passwd1 = request.form.get('password1') # Now a base64-encoded client-side hash
        
        passwd2 = request.form.get('password2') # Now a base64-encoded client-side hash

        # Check if the password passes ZXCVBN test and is actually Base64 Encoded

        # Otherwise IPv4address + username combination blacklisted using Blake2b

        try:
            test = base64.b64decode(passwd2)

        except ValueError:
            print("Base64 Decoding failure; Blacklisting [IPv4 address here]")

            return render_template('auth/register.html'),400

        if zxcvbn(str(test)).get('score') < 4:

            print("ZXCVBN test failure; Blacklisting [IPv4 address here]")

            return render_template('auth/register.html'),400


        # Checks if passwords match
        if passwd1 != passwd2 or passwd1 == None:
            flash('Password Error!', 'danger')
            return render_template('auth/register.html'),400

        server_salt = str(base64.b64encode(nacl.utils.random(size=64)))

        salted_hash = passwd2 + server_salt

        hashed_pass = nacl.hash.blake2b(bytes(salted_hash,'utf-8'),digest_size=64,encoder=nacl.encoding.URLSafeBase64Encoder)

        
        # Calls the User object from flask_app.models
        new_user = User(
       #     username=request.form.get('username'),
            first_name=request.form.get('fname'),
            last_name=request.form.get('lname'),
            email=request.form.get('email'),
            password=hashed_pass,
            salt=server_salt,
            permissions=1)
        

        # removed new_user.username 
        if user_exists(new_user.email):
            flash('User already exists!', 'danger')
            return render_template('auth/register.html'),400

        else:
#            recipients = ['notjoemartinez@protonmail.com']
#            for email in recipients:
#                msg = Message('Flask-Mail Test', sender = 'raiderHacksMail@gmail.com', recipients = [email])
#                msg.body = "{} {} would like to make an account on raiderHacks.com using {}".format(new_user.first_name, new_user.last_name, new_user.email)
#                mail.send(msg)
            # Insert new user into SQL
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            flash('Account created!', 'success')
            return redirect(url_for('index')),200


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    elif request.method == 'POST':
        # username = request.form.get('username')
        email = request.form.get('email')
        
        password_candidate = request.form.get('password')
        # Query for a user with the provided email 
        result = User.query.filter_by(email=email).first()

        if result is None:
            flash('Incorrect Login!', 'danger')
            return render_template('auth/login.html'),401
        
        else:
            salted_hash =  password_candidate + result.salt

            hash_verification = nacl.hash.blake2b(bytes(salted_hash,'utf-8'),digest_size=64,encoder=nacl.encoding.URLSafeBase64Encoder)
       
            if result.password == hash_verification:
                login_user(result)
                flash('Logged in!', 'success')
                return redirect(url_for('index')),200
            
            else:
                flash('Incorrect Login!', 'danger')
                return render_template('auth/login.html'),401
                
                 
        print(password_candidate, result, type(result))
        # If a user exsists and passwords match - login
#       if result is not None and sha256_crypt.verify(password_candidate, result.password):
#        if result is not None and 

            # Init session vars
#            login_user(result)
#            flash('Logged in!', 'success')
#            return redirect(url_for('index'))

#        else:
#            flash('Incorrect Login!', 'danger')
#            return render_template('auth/login.html')

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
