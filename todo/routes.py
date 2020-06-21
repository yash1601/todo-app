import os
import secrets
from flask import render_template,url_for, flash,  redirect, request, abort, session, jsonify
from todo.forms import LoginForm, RegistrationForm, UpdateForm, choices, TaskForm
from flask_login import login_user, current_user, logout_user, login_required
from todo.__init__ import db, app
from todo.models import User, Task


@app.route('/')
@app.route('/home', methods = ['POST', 'GET'])
@login_required
def home():
	form = TaskForm()
	list1 = Task.query.filter_by(category = 1)
	list2 = Task.query.filter_by(category = 2)
	list3 = Task.query.filter_by(category = 3)
	list4 = Task.query.filter_by(category = 4)
	if form.validate_on_submit():
		newtitle = form.title.data
		newpriority = form.priority.data
		newcategory = form.category.data
		task = Task()
		task.name = newtitle
		if newcategory == '1':
			task.category = 1
		elif newcategory == '2':
			task.category = 2
		elif newcategory == '3':
			task.category = 3
		elif newcategory == '4':
			task.category = 4

		if newpriority == '1':
			task.priority = 1
		elif newpriority == '2':
			task.priority = 2
		elif newpriority == '3':
			task.priority = 3
		
		task.author = current_user
		task.status = 1
		db.session.add(task)
		db.session.commit()
		return redirect(url_for('home'))

	return render_template('home.html', form = form, list1 = list1, list2 = list2, list3 = list3, list4 =list4)





@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		i = dict(choices).get(form.select.data)
		if i == "1":
			user = User(username = form.username.data, email=form.email.data, password = form.password.data, qint = 1, security_a = form.answer.data)
		else:
			user = User(username = form.username.data, email=form.email.data, password = form.password.data, qint = 2, security_a = form.answer.data)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! you can now log in!', 'success')
		return redirect(url_for('login'))
	else:
		flash('Unsuccessful, please try again', 'info')
	return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user and str(form.password.data) == str(user.password):
			login_user(user, remember = form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login Unsuccessful', 'danger')

	
	return render_template('login.html', title='Login', form=form)



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Info has been updated', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html', title='Account', form = form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))


@app.route("/full-list/<int:catname>", methods=['POST', 'GET'])
@login_required
def list(catname):
	data = Task.query.filter_by(category = catname)
	return render_template('full_list.html', title = 'full-list', data = data)