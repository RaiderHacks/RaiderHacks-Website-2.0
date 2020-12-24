from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    permissions = RadioField('Permissions:', choices=[(1,'Level 1: Everyone'),(2,'Level 2: Authenticated')], validators=[DataRequired()])
    submit = SubmitField('Post')
