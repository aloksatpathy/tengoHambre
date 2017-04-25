from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, Length, Regexp
from flask_wtf.file import FileField


class SigninForm(Form):
	email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password.")])
	submit = SubmitField("Sign in")

class CreateUserForm(Form):
	firstName = StringField('First Name', validators=[DataRequired("Please enter first name."), Length(min=2,max=25,message = "Inappropriate length for firstname"), Regexp(
         "^[a-zA-Z0-9]*$",
         message="Firstname can only contain letters and numbers"
      )])
	lastName = StringField('Last Name', validators=[DataRequired("Please enter last name."), Length(min=2,max=25,message = "Inappropriate length for lastname"), Regexp(
         "^[a-zA-Z0-9]*$",
         message="Lastname can only contain letters and numbers"
      )])
	email = StringField('Email ID', validators=[DataRequired("Please enter your email address."), Email("Please enter your valid email address.")])
	password = PasswordField('Password', validators=[DataRequired("Please enter your password."), Length(min=6, message="Password must be 6 characters or more.")])
	addressLine1 = StringField('Address Line1', validators=[DataRequired("Please enter your Address Line 1")])
	addressLine2 = StringField('Address Line2', validators=[DataRequired("Please enter your Address Line 2")])
	city = StringField('City', validators=[DataRequired("Please enter your City"), Length(min=2,max=30,message = "Inappropriate length for city")])
	state = StringField('City', validators=[DataRequired("Please enter your State"), Length(min=2,max=15,message = "Inappropriate length for state")])
	zipCode = IntegerField('Zip Code', validators=[DataRequired("Please enter your valid Zip Code")])
	country = StringField('Country', validators=[DataRequired("Please enter your Country")])
	phoneNumber = IntegerField('Address Line2', validators=[DataRequired("Please enter your valid Phone Number")])
	imageURL = FileField("Example File", validators=[DataRequired("Please provide your valid image")])
	submit = SubmitField("Sign Up")

class AddDishForm(Form):
	entreeName = StringField('Entree Name', validators=[DataRequired("Please enter the Entree name.")])
	price = DecimalField('Price in $', validators=[DataRequired("Please enter the price of the Entree.")])
	imageURL = FileField("Example File", validators=[DataRequired("Please provide your valid dish image ")])
	submit = SubmitField("Submit")

class AddRecipeForm(Form):
	recipeName = StringField('Recipe Name', validators=[DataRequired("Please enter the Recipe name.")])
	ingredients = TextAreaField('Ingredients', validators=[DataRequired("Please enter the ingredients for the recipe.")])
	directions = TextAreaField('Directions', validators=[DataRequired("Please enter the directions for the recipe.")])
	imageURL = FileField("Example File", validators=[DataRequired("Please provide your valid recipe image")])
	submit = SubmitField("Submit")