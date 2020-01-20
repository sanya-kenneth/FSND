import os
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from views import app_bp
from config import app_config
from models import db
from auth import AuthError


def create_app(environment):
  # create and configure the app
  app = Flask(__name__)
  app.config.from_object(app_config[environment])
  db.init_app(app)
  # Create database tables
  # db.drop_all(app=app)
  db.create_all(app=app)
  CORS(app)
  app.register_blueprint(app_bp)

  return app
