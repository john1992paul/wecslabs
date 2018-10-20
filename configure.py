import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Configure:
	SECRET_KEY = "treehasleaves1992"
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True
	MAIL_USERNAME = '########@gmail.com'
	MAIL_PASSWORD = '######'

	DB_PORT = 8182

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Configure):
	DEBUG = True

class TestConfig(Configure):
	TESTING = True

class ProductionConfig(Configure):
	DEBUG = False

configure = {
	'development': DevelopmentConfig,
	'testing': TestConfig,
	'prodution': ProductionConfig,
	'default' : DevelopmentConfig
}
