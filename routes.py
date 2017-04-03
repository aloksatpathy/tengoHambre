from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from forms import SigninForm, CreateUserForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tengohambre:tengohambre@tengohambredb.cwrcnfg5s8qa.us-west-2.rds.amazonaws.com/tengohambreDB'
db.init_app(app)

app.secret_key = "development-key"

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

			print(user.check_password(password))
			print(user.firstName)

			if user is not None and user.check_password(password):
				session['email'] = form.email.data
				invalidSignin=False
				return redirect(url_for('index'))
			else:
				invalidSignin=True
				return redirect(url_for('signin'))

	elif request.method == 'GET':
		return render_template('signin.html', form=form)




@app.route("/recipes")
def recipes():
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
			newuser=User(form.firstName.data, form.lastName.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email
			return redirect(url_for('index'))

	elif request.method == 'GET':
		return render_template("createUser.html", form=form)




@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))




if __name__ == "__main__":
	app.run(debug=True)