from datetime import datetime 
from todo.__init__ import db, app, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), unique = True, nullable = False)
	email = db.Column(db.String(120), unique = True, nullable = False)
	password = db.Column(db.String(60), nullable = False)
	qint = db.Column(db.Integer, default = 0)
	security_a = db.Column(db.String(200), nullable = False)
	tasks = db.relationship('Task', backref = 'author', lazy = True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"


class Task(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(20), unique = True, nullable = False)
	priority = db.Column(db.Integer, default = 0)
	category = db.Column(db.Integer, nullable = False)
	status = db.Column(db.Integer, default = 0)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
	date_posted = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

db.create_all()
