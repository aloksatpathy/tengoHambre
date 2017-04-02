from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://tengohambre:tengohambre@tengohambredb.cwrcnfg5s8qa.us-west-2.rds.amazonaws.com/tengohambreDB'
#db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
	return render_template("index.html")
	
@app.route("/signin")
def signin():
	return render_template("signin.html")
	
@app.route("/recipes")
def recipes():
	return render_template("demo.html")

if __name__ == "__main__":
	app.run(debug=True)