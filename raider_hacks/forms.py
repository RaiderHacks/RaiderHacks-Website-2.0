from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    permissions = RadioField('Permissions:', choices=[(1,'Level 1: Everyone'),(2,'Level 2: Authenticated')], validators=[DataRequired()])
    submit = SubmitField('Post')


class NewMember(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()]) 
    lname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Member')

    
