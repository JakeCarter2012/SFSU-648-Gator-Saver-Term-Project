import logging
import base64
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint, url_for, send_file

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os

from sfsuListings.aboutPage import aboutPage
from sfsuListings.loginSignUpPage import loginSignUpPage
from sfsuListings.results import searchResults
from sfsuListings.createPost import createPost
from sfsuListings.dashboard import dashboard

database_file = "sqlite:///postdatabase.db"

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])

app = Flask(__name__)

app.register_blueprint(aboutPage)
app.register_blueprint(loginSignUpPage)
app.register_blueprint(searchResults)
app.register_blueprint(createPost)
app.register_blueprint(dashboard)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

migrate = Migrate(app, db)
# NOTE: Secret key resets to new key each time server is restarted;
# this will invalidate any old session the user has, and requires log out
# can hardcode the secret key to 'solve' this, but is considered unsafe practice
app.config['SECRET_KEY'] = os.urandom(24)


if __name__ == '__main__':
    app.debug = True  # Turn on auto reloader and debugger
    app.config['SQLALCHEMY_ECHO'] = True  # Show SQL commands created
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.run()

from sfsuListings import models, routes
