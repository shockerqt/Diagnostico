DEBUG = True
SECRET_KEY = 'dev'
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:073tgpELbCEKiuwx@/formulario?unix_socket=./cloudsql/formulario-diagnostico:us-central1:formulario-db'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:073tgpELbCEKiuwx@localhost:3306/formulario'
SQLALCHEMY_TRACK_MODIFICATIONS = False
FLASK_ADMIN_SWATCH = 'cerulean'
CURRENCY_CONVERTER_KEY = '209275eb8048d95e2659'

# admin view
BASIC_AUTH_USERNAME = 'admin'
BASIC_AUTH_PASSWORD = '07bf9f48b4ef'