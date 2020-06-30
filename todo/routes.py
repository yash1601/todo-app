import os
import secrets
from flask import render_template,url_for, flash,  redirect, request, abort, session, jsonify
from todo.forms import LoginForm, RegistrationForm, UpdateForm, choices, TaskForm, SearchForm, choices2, PwdForm
from flask_login import login_user, current_user, logout_user, login_required
from todo.__init__ import db, app
from todo.models import User, Task


@app.route('/')
@app.route('/home', methods = ['POST', 'GET'])
@login_required
def home():
	form = TaskForm()
	list1 = Task.query.filter_by(category = 1, status = 1)
	list2 = Task.query.filter_by(category = 2, status = 1)
	list3 = Task.query.filter_by(category = 3, status = 1)
	list4 = Task.query.filter_by(category = 4, status = 1)
	list5 = Task.query.filter_by(status = 2)
	empty = 0
	if not list5:
		empty = 1
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

	return render_template('home.html', form = form, list1 = list1, list2 = list2, list3 = list3, list4 =list4, list5 = list5, empty = empty)





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
	return redirect(url_for('login'))


@app.route("/full-list/<catname>/<sort>/<name>", methods=['POST', 'GET'])
@login_required
def list(catname, sort, name):
	if name == '0':
		if sort == 'priority':
			data1 = Task.query.filter_by(category = catname, status = 1).order_by(Task.priority.desc()).all()
		elif sort == 'adding order' :
			data1 = Task.query.filter_by(category = catname, status = 1).order_by(Task.id.desc()).all()
		elif sort == 'none' :
			data1 = Task.query.filter_by(category = catname, status = 1)

	else :
		if sort == 'priority':
			data1 = Task.query.filter_by(name = name, category = catname, status = 1).order_by(Task.priority.desc()).all()
		elif sort == 'adding order':
			data1 = Task.query.filter_by(name = name, category = catname, status = 1).order_by(Task.id.desc()).all()
		elif sort == 'none' :
			data1 = Task.query.filter_by(name = name, category = catname, status = 1).all()

	form = SearchForm()
	num = catname
	if form.validate_on_submit():
		newname = form.name.data
		newnum = dict(choices2).get(form.sort.data)
		return redirect(url_for('list', catname = num, sort = newnum, name = newname))
	return render_template('full_list.html', title = 'full-list', data1 = data1, form = form)


@app.route("/checkoff/<int:test_id>", methods=['POST', 'GET'])
@login_required
def checkoff(test_id):
	task = Task.query.get(test_id)
	var = task.category
	setattr(task, "status", task.status+1)
	db.session.commit()
	flash('Item checked off', 'success')
	return redirect(url_for('home'))


@app.route("/clear", methods=['POST', 'GET'])
@login_required
def clear():
	tasks = Task.query.filter_by(status = 2)
	for i in tasks:
		db.session.delete(i)
		db.session.commit()

	return redirect(url_for('home'))


@app.route("/password", methods = ['POST', 'GET'])
def password():
	form = PwdForm()
	if form.validate_on_submit():
		if form.password1.data == form.password2.data:
			user = User.query.filter_by(email = form.email.data)
			if user:
				e = form.email.data
				user = User.query.filter_by(email = e).first()
				user.password = form.password1.data
				db.session.commit()
				logout_user()
				flash('password changed successfully, please try logging in again', 'info')
				return redirect(url_for('login'))
		else :
			flash('There was an error, please try again', 'info')
			return redirect(url_for('password'))

	return render_template('change_pwd.html', title='Change-password', form = form)