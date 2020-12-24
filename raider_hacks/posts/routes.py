from flask import Blueprint, render_template

from flask import render_template, request, redirect, url_for, flash
from flask import Blueprint, render_template
from passlib.hash import sha256_crypt
from sqlalchemy import or_
from flask_login import login_user, logout_user, login_required, current_user

from raider_hacks.forms import PostForm

from raider_hacks import app, db, mail, Message
from raider_hacks.models import User, Post


post_bp = Blueprint('post', __name__,
    template_folder='templates',
    static_folder='static'
)



@post_bp.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():

    result = User.query.filter_by(email=current_user.email).first()

    # if the admin feild is not true retun 404
    if result.permissions != 3:
        return "<h1> You do not have permissions to view this page</h1>" 
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, permissions=form.permissions.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('posts/create_post.html', title='New Post', form=form, legend='New Post', whoami=result)

@post_bp.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/post.html', title=post.title, post=post)

@post_bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts/create_post.html', title='Update Post', form=form, legend='Update Post')

@post_bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index'))
