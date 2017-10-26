from flask import Flask, url_for, redirect
from flask import session as login_session
from . import profile

@profile.route('/profile')
def profile_redirect():
	return redirect(url_for('profile.profile_page', titan_id=login_session['titan_id']))