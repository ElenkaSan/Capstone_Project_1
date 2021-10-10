"""Forms for our demo Flask app."""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,  PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, DataRequired, Optional, Length, Email, Length

class UserForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(message = 'Username is required')])
    password =  PasswordField('Password', validators=[InputRequired(), Length(min=3, message='Minimum of 3 characters required.')])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    notes = TextAreaField('Make Notes Here', validators = [Optional()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[InputRequired(message='Password required'), Length(min=3)])

class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    notes = TextAreaField('Make Notes Here', validators = [Optional()])

