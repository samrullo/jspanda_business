from wtforms import Form, StringField, PasswordField, validators, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
from flask_wtf import FlaskForm


class SignupForm(FlaskForm):
    """User Signup Form."""

    name = StringField('Name', render_kw={"class": "form-control"}, validators=[DataRequired(message=('Enter a fake name or something.'))])
    login = StringField('Login', render_kw={"class": "form-control"}, validators=[DataRequired(message=('Enter your desired login'))])
    email = StringField('Email', render_kw={"class": "form-control"},
                        validators=[Length(min=6, message=('Please enter a valid email address.')),
                                    Email(message=('Please enter a valid email address.')),
                                    DataRequired(message=('Please enter a valid email address.'))])
    password = PasswordField('Password', render_kw={"class": "form-control"},
                             validators=[DataRequired(message='Please enter a password.'),
                                         Length(min=6, message=('Please select a stronger password.')),
                                         EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Your Password', render_kw={"class": "form-control"})
    website = StringField('Website', render_kw={"class": "form-control"})
    submit = SubmitField('Register', render_kw={"class": "btn btn-lg btn-dark"})


class LoginForm(FlaskForm):
    """User Login Form."""
    login = StringField('Login', render_kw={"class": "form-control"}, validators=[DataRequired(message=('Enter your desired login'))])
    password = PasswordField('Password', render_kw={"class": "form-control"}, validators=[DataRequired('Uhh, your password tho?')])
    submit = SubmitField('Log In', render_kw={"class": "btn btn-lg btn-dark"})
