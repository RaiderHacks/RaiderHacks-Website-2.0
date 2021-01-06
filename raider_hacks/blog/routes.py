from flask import Blueprint, render_template
from flask_login import login_user, logout_user, login_required, current_user

from flask import current_app as app
from raider_hacks import app, db
from raider_hacks.models import User, Post

blog_bp = Blueprint('blog', __name__,
    template_folder='templates',
    static_folder='static'
)


@blog_bp.route("/blog")
def blog():

    # check to see if the user is logged in if this is the case return posts with the pemissions level 1
    if current_user.is_anonymous == True:
        posts = Post.query.filter(Post.permissions==1)
        return render_template("blog/blog.html", posts=reversed(posts), current_user=current_user) 
    else:
        # Now that we know the user is logged in we can create a user object 
        user = User.query.filter_by(email=current_user.email).first()
        # Render content for each permissions level  
        if user.permissions == 1: 
            posts = Post.query.filter(Post.permissions==1)
            return render_template("blog/blog.html", posts=reversed(posts), current_user=current_user) 

        elif user.permissions == 2:
            posts = Post.query.filter(or_(Post.permissions==1, Post.permissions==2))
            return render_template("blog/blog.html", posts=reversed(posts), current_user=current_user) 

        elif user.permissions == 3: 
            posts = Post.query.order_by(Post.date_posted).all()
            return render_template("blog/blog.html", posts=reversed(posts), current_user=current_user)
        else:
            return "<h1>Sorry {} Something went wrong and it was probably Tanveers falut<h1>".format(current_user)
