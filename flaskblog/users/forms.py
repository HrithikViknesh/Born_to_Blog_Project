from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed   # For image file field in User Account form
from wtforms import (StringField, PasswordField, BooleanField,
                     SubmitField, TextAreaField)    # form fields import
from wtforms.validators import (DataRequired, Length,
                                Email, EqualTo)     # validators import
from wtforms.validators import ValidationError      # for custom database validators definition
from flaskblog.models import User, Post             # DB Models
from flask_login import current_user                # for acc info update






class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField(label='Email', validators=[DataRequired(), Email()])

    password = PasswordField(label='Password', validators=[DataRequired()])

    confirm_password = PasswordField(label='Confirm-Password', validators=[DataRequired(), EqualTo(
        'password')])  # IMportant: variable name , not label nmae

    submit = SubmitField(label='Sign Up')

    def validate_username(self, username):

        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('This username has already been taken. Please choose a different one')

    def validate_email(self, email):

        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError('An account with this email id already exists. Please proceed to Log In')


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])

    password = PasswordField(label='Password', validators=[DataRequired()])

    remember = BooleanField(label='Remember_me')

    submit = SubmitField(label='Log In')


# Form to update user account information

class UpdateAccountForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField(label='Email', validators=[DataRequired(), Email()])

    picture = FileField(label='Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField(label='Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            existing_user = User.query.filter_by(username=username.data).first()
            if existing_user:
                raise ValidationError('This username has already been taken. Please choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            existing_email = User.query.filter_by(email=email.data).first()
            if existing_email:
                raise ValidationError('An account with this email id already exists.')


# Form to submit email in order to get reset password link
class RequestResetForm(FlaskForm):
    email = StringField(label='Email',
                        validators=[DataRequired(), Email()])

    submit = SubmitField(label='Request Password Reset')

    # check if an account with such email address exists
    """
    Parts of it have been commented to avoid enumeration attacks
    """
    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        # if existing_email is None:
        #     raise ValidationError('There is no account with that email address. Please recheck or proceed to Register '
        #                           'a new account')


# Form to fill out new password
class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired()])

    confirm_password = PasswordField(label='Confirm-Password', validators=[DataRequired(), EqualTo(
        'password')])  # Important: variable name , not label nmae

    submit = SubmitField(label='Reset Password')
