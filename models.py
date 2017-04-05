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
	addressLine1 = db.Column(db.String(50))
	addressLine2 = db.Column(db.String(50))
	city = db.Column(db.String(30))
	state = db.Column(db.String(30))
	zipCode = db.Column(db.String(30))
	country = db.Column(db.String(30))
	phoneNumber = db.Column(db.String(30))
	imageURL = db.Column(db.String(300))

	def __init__(self, firstName, lastName, email, password, addressLine1, addressLine2, city, state, zipCode, country, phoneNumber, imageURL):
		self.firstName = firstName.title()
		self.lastName = lastName.title()
		self.email = email.lower()
		self.set_password(password)
		self.addressLine1 = addressLine1
		self.addressLine2 = addressLine2
		self.city = city
		self.state = state
		self.zipCode = zipCode
		self.country = country
		self.phoneNumber = phoneNumber
		self.imageURL = imageURL
		
	def set_password(self, password):
		self.password = hashlib.sha1(password.encode()).hexdigest()
		# self.password = generate_password_hash(password)

	def check_password(self, password):
		# return check_password_hash(self.password, password)
		# hash_object=hashlib.sha1(str(password))
		password_hash = hashlib.sha1(password.encode()).hexdigest()
		# #return generate_password_hash(password)
		return self.password==password_hash 