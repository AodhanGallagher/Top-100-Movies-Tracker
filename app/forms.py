# Importing relevant modules
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

# Creating a registration form that will be used for entering data into the user table
class RegistrationForm(FlaskForm):
    forename = StringField('First Name', validators=[DataRequired(), Length(min=1, max=20, message="First name cannot exceed 20 characters")])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=1, max=25, message="Surname cannot exceed 25 characters")])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20, message="Username cannot exceed 20 characters")])
    email = StringField('Email Address', validators=[DataRequired(), Length(min=1, max=50, message="Email cannot exceed 50 characters")])
    password = PasswordField('New Password', validators=[
                                            DataRequired(),
                                            Length(min=5, max=25, message="Password must be between 5 and 25 characters"),
                                            EqualTo('confirmPassword', message="Passwords must match")
                                            ])
    confirmPassword = PasswordField('Confirm Password')

# Creating a login form that will be used to check values against the user database to log a user in to their account
class LoginForm(FlaskForm):
    loginUsername = StringField('Username', validators=[DataRequired(), Length(min=1, max=20, message="Username cannot exceed 20 characters")])
    loginPassword = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=25, message="Password must be between 5 and 25 characters")])