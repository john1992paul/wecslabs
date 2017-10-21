from flask import Flask, render_template
from flask import session as login_session
import json
import random
import string
from . import auth
# --------------------------------------------------Show SignIn page ---------------------------------------------------- #
@auth.route('/login', methods = ['GET'])
def showlogin():
	try:
		if login_session['username']:
			return 'Already logged in'
	except:
		state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
		login_session['state'] = state
		return render_template('auth/auth.html', STATE=state)
