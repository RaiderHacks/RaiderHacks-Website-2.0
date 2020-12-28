from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from passlib.hash import sha256_crypt
from sqlalchemy import or_

from raider_hacks import app, db, mail, Message
from raider_hacks.models import User, Post
from raider_hacks.forms import PostForm



@app.route("/")
def index():
    db.create_all()
    return render_template("index.html")

@app.route("/members")
def meetmembers():
    return render_template("members.html")


@app.route("/achievements")
def achievements():
    return render_template("achievements.html")

@app.route("/addachievements")
def addachievements():
    return render_template("addachievements.html")


@app.route("/about")
def about():
    return render_template("about.html")



