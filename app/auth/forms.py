from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.fields import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import ValidationError
from ..models import User

class SigninForm(FlaskForm):
    email = EmailField('Email', [DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField('Sign in')

class SignupForm(FlaskForm):
    email = EmailField('Email', [DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', [DataRequired(), Length(1, 64)])
    password = PasswordField('Password', [DataRequired()])
    password2 = PasswordField('Password Confirm', [DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered!')

class SettingForm(FlaskForm):
    username = StringField('Username', [DataRequired(), Length(1, 64)])
    password = PasswordField('New Password', [DataRequired()])
    password2 = PasswordField('New Password Confirm', [DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')