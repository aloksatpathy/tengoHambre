from flask import Flask, render_template, flash, request, session, redirect, url_for, flash
from flask_wtf import Form
from models import db, User
from forms import SigninForm, CreateUserForm, AddDishForm, AddRecipeForm

#import os
import config


from uuid import uuid4
import boto
import os.path
from flask import current_app as app
from werkzeug.utils import secure_filename



from sqlalchemy import create_engine

connection_string='mysql+pymysql://tengohambre:tengohambre@tengohambredb.cwrcnfg5s8qa.us-west-2.rds.amazonaws.com/tengohambreDB'
engine = create_engine(connection_string)
engine.echo=False


imageAWS="https://s3-us-west-1.amazonaws.com/tengohambreimages/tengohambre/"




app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tengohambre:tengohambre@tengohambredb.cwrcnfg5s8qa.us-west-2.rds.amazonaws.com/tengohambreDB'
db.init_app(app)

app.config.from_object('config')

app.secret_key = "development-key"



def s3_upload(source_file, upload_dir=None, acl='public-read'):
	if upload_dir is None:
		upload_dir = 'tengohambre'
		#upload_dir = app.config["S3_UPLOAD_DIRECTORY"]

	source_filename = secure_filename(source_file.data.filename)
	source_extension = os.path.splitext(source_filename)[1]

	destination_filename = uuid4().hex + source_extension

	# Connect to S3 and upload file.
	#conn = boto.connect_s3('','')
	conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'))


	b = conn.get_bucket('tengohambreimages')#os.environ.get('S3_BUCKET')

	sml = b.new_key("/".join([upload_dir, destination_filename]))
	sml.set_contents_from_string(source_file.data.read())
	sml.set_acl(acl)

	return destination_filename




@app.route("/")
def index():
	return render_template("index.html")



@app.route("/signin", methods=["GET", "POST"])
def signin():
	if 'email' in session:
		return redirect(url_for('index'))
	
	form = SigninForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("signin.html", form=form)
		else:
			email = form.email.data
			password = form.password.data

			user = User.query.filter_by(email=email).first()

			#print(user.check_password(password))
			#print(user.firstName)

			if user is None:
				passmatch = False
			else:
				passmatch = user.check_password(password)

			if user is not None and passmatch == True:
				session['email'] = form.email.data
				session['firstName'] = user.firstName


				sql_get_userID="SELECT userID from User WHERE email='%s'" % (session['email'])
				print(sql_get_userID)

				with engine.connect() as con:
					rs=con.execute(sql_get_userID)

				userRow=rs.fetchone()

				session['userID'] = userRow[0]

				return redirect(url_for('index'))
			elif user is None and passmatch==False:
				flash ("Sorry, the email ID entered is invalid")
				return redirect(url_for('signin'))
			elif user is not None and passmatch==False:
				flash ("Sorry, the password entered is invalid")
				return redirect(url_for('signin'))
	elif request.method == 'GET':
		return render_template('signin.html', form=form)




@app.route("/recipes")
def recipes():
	recipes_list = []
	with engine.connect() as con:
		rs=con.execute('SELECT recipeName,image,recipeIngredients,recipeDirections FROM Recipes')

		for row in rs:
			recipes_list.append(row)
			#print(row[2],'\n')

		return render_template("demo.html", rs=recipes_list)

	return render_template("demo.html")


@app.route("/createUser", methods=["GET", "POST"])
def createUser():
	if 'email' in session:
		return redirect(url_for('index'))

	form = CreateUserForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("createUser.html", form=form)
		else:
			if User.is_email_taken(form.email.data):
				flash ("Sorry, the email id is already taken") 
				return render_template("createUser.html", form=form)
			else:
				output = s3_upload(form.imageURL)

				imageFullPath = imageAWS + output

				newuser=User(form.firstName.data, form.lastName.data, form.email.data, form.password.data, form.addressLine1.data, form.addressLine2.data, form.city.data, form.state.data, form.zipCode.data, form.country.data, form.phoneNumber.data, imageFullPath)
				db.session.add(newuser)
				db.session.commit()

				session['email'] = newuser.email
				session['firstName'] = newuser.firstName

				sql_get_userID="SELECT userID from User WHERE email='%s'" % (session['email'])
				print(sql_get_userID)

				with engine.connect() as con:
					rs=con.execute(sql_get_userID)

				userRow=rs.fetchone()

				session['userID'] = userRow[0]
				return redirect(url_for('index'))

	elif request.method == 'GET':
		return render_template("createUser.html", form=form)


@app.route("/AddDish", methods=["GET", "POST"])
def AddDish():
	if 'email' not in session:
		return redirect(url_for('index'))

	form = AddDishForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("AddDish.html", form=form)
		else:
			output = s3_upload(form.imageURL)

			imageFullPath = imageAWS + output

			sql_query="INSERT INTO Dish (userID, dishName, imageURL, price) VALUES ((SELECT userID FROM User WHERE email='%s'), '%s', '%s', %s)" % (session['email'], form.entreeName.data, imageFullPath, form.price.data)
			print(sql_query)

			with engine.connect() as con:
				rs=con.execute(sql_query)

			return redirect(url_for('chefProfile',userID=session['userID']))

	elif request.method == "GET":
		return render_template("AddDish.html", form=form)


@app.route("/chefProfile")
def chefProfile():
	#if 'email' not in session:
	#	return redirect(url_for('index'))

	userID = request.args.get('userID', None)
	print(userID)

	chef_info = []
	dish_list = []
	recipe_list = []

	sql_query_chef="SELECT firstName,lastName,email,addressLine1,addressLine2,city,state,zipCode,phoneNumber,imageURL,userID from User where userID=%s"%(userID)
	print(sql_query_chef)

	with engine.connect() as con:
		rs=con.execute(sql_query_chef)

	for row in rs:
		chef_info.append(row)

	sql_query_dish="SELECT dishName, imageURL, price FROM Dish WHERE userID=%s"%(userID)
	print(sql_query_dish)

	with engine.connect() as con:
		rs=con.execute(sql_query_dish)

	for row in rs:
		dish_list.append(row)



	sql_query_recipe="SELECT recipeName, image, recipeIngredients, recipeDirections FROM Recipes WHERE userID=%s"%(userID)
	print(sql_query_recipe)

	with engine.connect() as con:
		rs=con.execute(sql_query_recipe)

	for row in rs:
		recipe_list.append(row)

	return render_template("chefProfile.html", chef=chef_info, rs=dish_list, recipe=recipe_list)




@app.route("/chefConnect")
def chefConnect():
	chef_list = []

	sql_query_chef="SELECT firstName, lastName, imageURL, userID from User"
	print(sql_query_chef)

	with engine.connect() as con:
		rs=con.execute(sql_query_chef)
	
	for row in rs:
		chef_list.append(row)
		print(row)

	return render_template("chefcarousel.html", chef_list=chef_list)



@app.route("/logout")
def logout():
	session.pop('email', None)
	session.pop('firstName', None)
	session.pop('userID', None)
	return redirect(url_for('index'))

@app.route('/contactus')
def contactus():
    return render_template('Contactus.html')


@app.route('/deleteProfile')
def deleteProfile():
	sql_query_delete_Profile="DELETE FROM Recipes WHERE userID=(SELECT userID FROM User WHERE email='%s'); DELETE FROM Dish WHERE userID=(SELECT userID FROM User WHERE email='%s'); DELETE FROM User WHERE email='%s';"%(session['email'], session['email'], session['email'])
	print(sql_query_delete_Profile)

	with engine.connect() as con:
		rs=con.execute(sql_query_delete_Profile)

	return redirect(url_for('logout'))


@app.route('/addRecipe', methods=["GET", "POST"])
def addRecipe():
	if 'email' not in session:
		return redirect(url_for('index'))

	form = AddRecipeForm()

	if request.method == "POST":
		if form.validate() == False:
			return render_template("AddRecipe.html", form=form)
		else:
			output = s3_upload(form.imageURL)

			imageFullPath = imageAWS + output

			ingredients=form.ingredients.data
			ingredients=ingredients.replace('\n', '<br>')

			directions=form.directions.data
			directions=directions.replace('\n', '<br>')


			sql_query="INSERT INTO Recipes (userID, recipeName, recipeIngredients, recipeDirections, image) VALUES (%s, '%s', '%s', '%s', '%s')" % (session['userID'], form.recipeName.data, ingredients, directions, imageFullPath)
			print(sql_query)

			with engine.connect() as con:
				rs=con.execute(sql_query)

			return redirect(url_for('chefProfile',userID=session['userID']))

	elif request.method == 'GET':
		return render_template("AddRecipe.html", form=form)	


if __name__ == "__main__":
	app.run(debug=True)