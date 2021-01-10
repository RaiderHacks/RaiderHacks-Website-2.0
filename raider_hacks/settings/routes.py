from flask import Blueprint, render_template, request, redirect, url_for, flash 
from flask_login import login_user, logout_user, login_required, current_user

from raider_hacks import app, db, mail, Message
from raider_hacks.models import User, Post


settings_bp = Blueprint('settings', __name__,
            template_folder='templates',
)

@settings_bp.route("/settings/profile", methods=["POST","GET"])
@login_required
def settings():

    return render_template("settings/profile.html")


    # user = User.query.filter_by(email=current_user.email).first()

