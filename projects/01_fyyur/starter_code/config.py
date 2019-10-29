import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

WHOOSH_BASE = 'whoosh'


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://postgres:psql@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS = False
