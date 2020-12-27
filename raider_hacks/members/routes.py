import os, secrets
from PIL import Image
from flask import Blueprint, render_template, url_for, flash, request

# import member form
from raider_hacks.forms import NewMember
# import db modles 
from raider_hacks.models import Member
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

        output_size = (125,125)
        i = Image.open(form_image)
        i.thumbnail(output_size)
        i.save(image_path)

        return image_fn

@members_bp.route("/member/<int:member_id>")
def member(member_id):
        member = Member.query.get_or_404(member_id)
        return render_template('members/member.html', member=member)



@members_bp.route("/member/new", methods=['GET', 'POST'])
def make_member():
        form = NewMember()
        if request.method == 'POST' and form.validate_on_submit:
                # image_file = ''
                # if form.profile_pic.data:
                        # image_file = save_image(form.profile_pic.data)
                        # print("TEST LINE 44: ",image_file)
                print('TEST LINE 45: ',form.profile_pic.data)
                image_file = save_image(form.profile_pic.data)
                print("TEST LINE 47: ",image_file)
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