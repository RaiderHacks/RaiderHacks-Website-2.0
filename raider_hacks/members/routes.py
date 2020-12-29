import os, secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, request, redirect 
from flask_login import login_user, logout_user, login_required, current_user

# import member form
from raider_hacks.forms import NewMember
# import db modles 
from raider_hacks.models import Member, User
# import actual db
from raider_hacks import db, app


members_bp = Blueprint( 'members', __name__,
        template_folder='templates',
        static_folder='static'
)


@members_bp.route("/members") 
def members():
        members = Member.query.all()
        return render_template('members/members.html', members=members)

def save_image(form_image):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_image.filename)
        image_fn = random_hex + f_ext
        image_path = os.path.join(app.root_path, 'static/images/profile_pics', image_fn)

        output_size = (500,500)
        i = Image.open(form_image)
        i.thumbnail(output_size)
        i.save(image_path)

        return image_fn

@members_bp.route("/member/<int:member_id>")
def member(member_id):

        member = Member.query.get_or_404(member_id)
        user = ''

        if current_user.is_anonymous == False:

                user = User.query.filter_by(email=current_user.email).first()
                return render_template('members/member.html', member=member, user=user)

        else:
                return render_template('members/member.html', member=member, user=user)



@members_bp.route("/member/new", methods=['GET', 'POST'])
@login_required
def make_member():

        result = User.query.filter_by(email=current_user.email).first()
        # if the admin feild is not true retun 404
        if result.permissions != 3:
                return "<h1> You do not have permissions to view this page</h1>" 

        form = NewMember()
        if request.method == 'POST' and form.validate_on_submit:

                image_file = save_image(form.profile_pic.data)

                # build member from form data
                member = Member(
                fname=form.fname.data, 
                lname=form.lname.data, 
                email=form.email.data, 
                bio=form.bio.data, 
                profile_pic=image_file)
                # add member to database 
                db.session.add(member)
                db.session.commit()
                flash('You added a member', 'success')
        elif request.method == 'GET':
                return render_template('members/new_member.html', form=form)

        return render_template('members/new_member.html', form=form)


@members_bp.route("/member/<int:member_id>/update", methods=['GET', 'POST'])
@login_required
def update_member(member_id):
        # check user permissions
        result = User.query.filter_by(email=current_user.email).first()
        # if the admin feild is not true retun 404
        if result.permissions != 3:
                return "<h1> You do not have permissions to view this page</h1>" 

        # queary the member data using the member id
        member = Member.query.get_or_404(member_id) 
        form = NewMember()
        if form.validate_on_submit and request.method == 'POST': 

                image_file = save_image(form.profile_pic.data)
                member.fname = form.fname.data
                member.lname = form.lname.data
                member.email = form.email.data
                member.bio = form.bio.data
                member.profile_pic = image_file 

                db.session.commit()
                flash('Your post has been updated!', 'success')
                return redirect(url_for('members.member', member_id=member.id))

        # populate the form data using the data we quiered from the member_id 
        elif request.method == 'GET':
                form.fname.data = member.fname
                form.lname.data = member.lname
                form.email.data = member.email 
                form.bio.data = member.bio 
                form.profile_pic.data = member.profile_pic 

        return render_template('members/new_member.html', form=form)

@members_bp.route("/member/<int:member_id>/delete", methods=['POST'])
@login_required
def delete_member(member_id):
        # check user permmisions
        result = User.query.filter_by(email=current_user.email).first()
        # if the admin feild is not true retun 404
        if result.permissions != 3:
                return "<h1> You do not have permissions to view this page</h1>" 

        member = Member.query.get_or_404(member_id)
        
        db.session.delete(member)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('index'))