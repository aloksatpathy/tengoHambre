from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField

class SigninForm(Form):
	email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
	submit = SubmitField("Sign in")

class CreateUserForm(Form):
	firstName = StringField('First Name', validators=[DataRequired("Please enter first name.")])
	lastName = StringField('Last Name', validators=[DataRequired("Please enter last name.")])
	email = StringField('Email ID', validators=[DataRequired("Please enter your email address."), Email("Please enter your valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password."), Length(min=6, message="Password must be 6 characters or more.")])
	addressLine1 = StringField('Address Line1', validators=[DataRequired("Please enter your Address Line 1")])
	addressLine2 = StringField('Address Line2', validators=[DataRequired("Please enter your Address Line 2")])
	city = StringField('City', validators=[DataRequired("Please enter your City")])
	state = StringField('City', validators=[DataRequired("Please enter your State")])
	zipCode = StringField('Zip Code', validators=[DataRequired("Please enter your Zip Code")])
	country = StringField('Country', validators=[DataRequired("Please enter your Country")])
	phoneNumber = StringField('Address Line2', validators=[DataRequired("Please enter your Phone Number")])
	imageURL = FileField("Example File")
	submit = SubmitField("Sign Up")

class AddDishForm(Form):
	entreeName = StringField('Entree Name', validators=[DataRequired("Please enter the Entree name.")])
	price = StringField('Price in $', validators=[DataRequired("Please enter the price of the Entree.")])
	imageURL = FileField("Example File")
	submit = SubmitField("Submit")