from flask import Flask
from app.config import configuration


def create_app(environment):
	app = Flask(__name__)
	app.config.from_object(configuration[environment])

	from app.views.views import mod

	app.register_blueprint(mod, url_prefix = '/api/v1')

	return app
