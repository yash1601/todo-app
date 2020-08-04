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

choices2 = [
		("1", 'priority'),
		("2", 'adding order'),
		("3", 'none')
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
	category = RadioField('Category:',validators=[DataRequired()], choices = [('1','Personal'),('2','Work'),('3','Shopping'),('4','Others')])
	priority = RadioField('priority:', validators=[DataRequired()], choices = [('1','Urgent'),('2','Short Term'),('3','Long Time')])
	submit = SubmitField('add task')


class SearchForm(FlaskForm):
	name = StringField('name: ', validators=[Length(min=2, max=20)])
	sort = RadioField('sort by:(please select)', choices = [('1','priority'),('2','adding order'), ('3','none')])
	submit = SubmitField('Go')

class PwdForm(FlaskForm):
	email = StringField('Enter your Email', validators=[DataRequired(), Email()])
	password1 = PasswordField('New Password', validators=[DataRequired()])
	password2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField('change password')
	def validate_password(self, password1, password2):
		if(password1.data != password2.data):
			raise ValidationError('Passwords do not match, please try again')
	
	def validate_username(self, email):
		user = User.query.filter_by(email=email.data).first()
		if not user:
			raise ValidationError('This email does not exist, please try again')

