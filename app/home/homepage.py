from flask import render_template, request, redirect, url_for
from flask import session as login_session
from . import home

@home.route('/')
def homepage():
	try:
		message = login_session['message']
	except:
		message = ''
	return render_template('home/homepage.html', message = message)

@home.route('/confirm', methods=['POST'])
def confirm():
	secret_key = request.form['secret_key']
	if secret_key == 'luttapi':
		return redirect(url_for('auth.showlogin'))
	else:
		login_session['message'] = "Access Denied"
		return redirect(url_for("home.homepage"))

@home.route('/delete', methods=['POST'])
def delete():
	print('delete is working')
	del login_session['message']
	return 'deleted'