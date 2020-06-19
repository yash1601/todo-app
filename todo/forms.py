from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from todo.models import User
from flask_login import current_user


choices = [
		("1", 'name of your first pet:'),
		("2", 'name of that special someone:'),
	]

class RegistrationForm(FlaskForm):
	
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	select = SelectField('Select security question', choices=choices, default = None)
	answer = StringField('Answer to the selected question:', validators=[DataRequired()])
	submit = SubmitField('Sign up')


	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('This username is taken, please try for another')

	def validate_username(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('This email is taken, please try for another')



class LoginForm(FlaskForm):

	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')



class UpdateForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('This username is taken, please try for another')


class TaskForm(FlaskForm):
	title = StringField('enter task name here:', validators=[DataRequired(), Length(min=2, max=20)])
	category = RadioField('Category:', choices = [('1','Personal'),('2','Work'),('3','Shopping'),('4','Others')])
	priority = RadioField('priority:', choices = [('1','Urgent'),('2','Short Term'),('3','Long Time')])
	submit = SubmitField('add task')