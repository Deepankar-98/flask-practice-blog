from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_app.database_model import User, Post
from flask_login import current_user


class RegistrationForm (FlaskForm):
    username = StringField("Username *", validators = [DataRequired(), Length(min=3, max=20)])
    email = StringField("Email *", validators=[DataRequired(), Email()])
    password = PasswordField("Password *", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password *", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username (self, username):
        if User.query.filter_by(username= username.data).first():
            raise ValidationError('Username already taken. Please enter another username.')

    def validate_email (self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email Id already in use. Please enter another Email Id or Log In to your account.')


class LoginForm (FlaskForm):
    email = StringField("Email:", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm (FlaskForm):
    username = StringField("Username *", validators = [DataRequired(), Length(min=3, max=20)])
    email = StringField("Email *", validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','jpeg', 'png'])])
    submit = SubmitField("Update")

    def validate_username (self, username):
        if current_user.username != username.data:
            if User.query.filter_by(username= username.data).first():
                raise ValidationError('Username already taken. Please enter another username.')

    def validate_email (self, email):
        if current_user.email != email.data:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError('Email Id already in use. Please enter another Email Id or Log In to your account.')