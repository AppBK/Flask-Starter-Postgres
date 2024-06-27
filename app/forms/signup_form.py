from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User

import re

def user_exists(form, field):
    # Checking if user exists
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('Email address is already in use.')


def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')

def username_length_compliance(form, field):
    if len(field.data) > 40 or len(field.data) == 0:
        raise ValidationError('Username must have a length of 1-40 characters.')

def is_valid_email(form, field):
    email = field.data
    # Regular expression pattern for validating an email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Use re.match to check if the provided email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        raise ValidationError('Please enter a valid email.')

def password_min_len(form, field):
    password = field.data

    if len(password) < 8:
        raise ValidationError('Password must have a minimum length of 8 characters.')


class SignUpForm(FlaskForm):
    username = StringField(
        'username', validators=[DataRequired(), username_length_compliance, username_exists])
    email = StringField('email', validators=[DataRequired(), is_valid_email, user_exists])
    password = StringField('password', validators=[DataRequired(), password_min_len])
