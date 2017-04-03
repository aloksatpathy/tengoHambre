from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SigninForm(Form):
	email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
	submit = SubmitField("Sign in")

class CreateUserForm(Form):
	firstName = StringField('First Name', validators=[DataRequired("Please enter your first name.")])
	lastName = StringField('Last Name', validators=[DataRequired("Please enter your last name.")])
	email = StringField('Email ID', validators=[DataRequired("Please enter your email address."), Email("Please enter your valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password."), Length(min=6, message="Password must be 6 characters or more.")])
	submit = SubmitField("Sign Up")