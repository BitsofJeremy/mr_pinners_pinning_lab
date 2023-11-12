# config.py

import os
from datetime import timedelta

# Put any configurations here that are common across all environments

# App Version Number
APP_VERSION = '0.0.7'

# Name of the app
APP_NAME = 'app'
HOST = '0.0.0.0'
PORT = '5000'

# Get our environment
FLASK_ENV = os.getenv('FLASK_ENV')
# Set debug mode
if FLASK_ENV == 'production':
    DEBUG = False
else:
    DEBUG = True

# Some Flask App Config settings
SESSION_COOKIE_NAME = 'Mr_Pinners_Pinning_lab'
# SESSION_COOKIE_SECURE = True

# Session timeout set to 4 hours
PERMANENT_SESSION_LIFETIME = timedelta(hours=4)

# SQLite DB info
# TODO Add MySQL connections for Production
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'pinning_lab.db')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Upload Config
# allow for IMAGES up to 10mb
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024

# Threads
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = os.urandom(32).hex()

# Secret key for signing cookies
SECRET_KEY = os.urandom(32).hex()

# Celery configuration
CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

# Blockfrost API
BLOCKFROST_IPFS = os.getenv('BLOCKFROST_IPFS')

