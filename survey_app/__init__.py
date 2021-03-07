from flask import Flask, session, redirect, Response
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from .models import db, User, UserRecommendations, RecommendationsTable, ModelS1, ModelS2, ModelS2Products, ModelS3, ModelS4, ModelS5, ModelS6, ModelS7, ModelSp1, ModelSp2, ModelSp3, ModelSp4


def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	
	# load config
	app.config.from_object('config')
	app.config.from_pyfile('config.py', silent=True)
	
	# load database
	from .models import db
	db.init_app(app)
	with app.app_context():
		db.create_all()
	
	# load blueprints
	from . import blueprints
	app.register_blueprint(blueprints.bp)

	# admin auth
	basic_auth = BasicAuth(app)

	# admin
	admin = Admin(app, template_mode='bootstrap3')

	# login failed handler, from:
	class AuthException(HTTPException):
		def __init__(self, message):
			super().__init__(message, Response(
				message, 401,
				{'WWW-Authenticate': 'Basic realm="Login Required"'}
			))

	# overwrite ModelView of flask_admin to just affects admin page
	class SecureModelView(ModelView):
		def is_accessible(self):
			if not basic_auth.authenticate():
				raise AuthException('Not authenticated. Refresh the page.')
			else:
				return True

		def inaccessible_callback(self, name, **kwargs):
			return redirect(basic_auth.challenge())

	class SurveyView(SecureModelView):
		inline_models = (UserRecommendations, ModelS1, ModelS2, ModelS2Products, ModelS3, ModelS4, ModelS5, ModelS6, ModelS7, ModelSp1, ModelSp2, ModelSp3, ModelSp4)
		can_export = True

	admin.add_view(SurveyView(User, db.session, category='Survey'))
	admin.add_view(SecureModelView(ModelS1, db.session, category='Survey'))
	admin.add_view(SecureModelView(ModelS2, db.session, category='Survey'))
	admin.add_view(SecureModelView(ModelS2Products, db.session, category='Survey'))
	admin.add_view(SecureModelView(ModelS3, db.session, category='Survey'))
	admin.add_view(SecureModelView(ModelS4, db.session, category='Survey'))
	admin.add_view(SecureModelView(ModelS5, db.session, category='Survey'))
	admin.add_view(SecureModelView(ModelS6, db.session, category='Survey'))
	admin.add_view(SecureModelView(ModelS7, db.session, category='Survey'))
	admin.add_view(SecureModelView(UserRecommendations, db.session, category='Survey'))
	

	return app