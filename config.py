import os
from datetime import timedelta

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TESTS_DIR = BASE_DIR + "/tests"

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(TESTS_DIR, 'test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = "secret"

SECRET_KEY = "secret"

JWT_DEFAULT_REALM = 'Login Required'
JWT_AUTH_USERNAME_KEY = 'email'
JWT_AUTH_URL_RULE = '/auth/login'
JWT_EXPIRATION_DELTA = timedelta(seconds=3600)
