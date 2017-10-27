from flask import Flask
from flask_mail import Mail
from configure import configure

mail = Mail()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(configure[config_name])
	configure[config_name].init_app(app)

	mail.init_app(app)

	from .home import home as home_blueprint
	app.register_blueprint(home_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint)

	from .profile import profile as profile_blueprint
	app.register_blueprint(profile_blueprint)

	from .project import project as project_blueprint
	app.register_blueprint(project_blueprint)

	from .teambase import teambase as teambase_blueprint
	app.register_blueprint(teambase_blueprint)

	return app