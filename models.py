from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
import hashlib

db = SQLAlchemy()

class User(db.Model):
	__tablename__='User'
	firstName = db.Column(db.String(30))
	lastName = db.Column(db.String(30))
	email = db.Column(db.String(30), primary_key=True)
	password = db.Column(db.String(54))

	def __init__(self, firstName, lastName, email, password):
		self.firstName = firstName.title()
		self.lastName = lastName.title()
		self.email = email.lower()
		self.set_password(password)
		
	def set_password(self, password):
		self.password = hashlib.sha1(password.encode()).hexdigest()
		# self.password = generate_password_hash(password)

	def check_password(self, password):
		# return check_password_hash(self.password, password)
		# hash_object=hashlib.sha1(str(password))
		password_hash = hashlib.sha1(password.encode()).hexdigest()
		# #return generate_password_hash(password)
		return self.password==password_hash 