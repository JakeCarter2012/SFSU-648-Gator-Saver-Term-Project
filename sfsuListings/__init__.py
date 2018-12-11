import logging
import base64

import sqlite3
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint, url_for

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import  secure_filename
from flask_migrate import Migrate
import os

from sfsuListings.aboutPage import aboutPage
from sfsuListings.loginSignUpPage import loginSignUpPage
from sfsuListings.results import searchResults
from sfsuListings.createPost import createPost
database_file = "sqlite:///postdatabase.db"

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['jpg', 'png'])

app = Flask(__name__)

app.register_blueprint(aboutPage)
app.register_blueprint(loginSignUpPage)
app.register_blueprint(searchResults)
app.register_blueprint(createPost)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

migrate = Migrate(app, db)
# NOTE: Secret key resets to new key each time server is restarted;
# this will invalidate any old session cookies the user has, and requires log out
# can hardcode the secret key to 'solve' this, but is considered unsafe practice
app.config['SECRET_KEY'] = os.urandom(24)


# model class
class Posts(db.Model):
    name = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
    author = db.Column(db.String(80), unique=False, nullable=True, primary_key=False)
    price = db.Column(db.REAL, unique=False, nullable=False, primary_key=False)
    description = db.Column(db.String(300), unique=False, nullable=False, primary_key=False)
    image = db.Column(db.String(80), unique=False, nullable=True, primary_key=False)
    id = db.Column(db.INTEGER, unique=True, nullable=False, primary_key=True)
    category = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    approval = db.Column(db.String(20), unique=False, nullable=False, primary_key=False)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Name: {}>".format(self.name)
        return "<Author: {}".format(self.author)
        return "<id: {}".format(self.id)
        return "<price: {}".format(self.price)
        return "<image: {}".format(self.image)
        return "<category: {}".format(self.category)

class Admin(db.Model):
    AdminName = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    password_hash = db.Column(db.String(96), unique=False, nullable=False, primary_key=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Username: {}>".format(self.UserName)
        return "<Hashed Password: {}".format(self.password_hash)

class Messages(db.Model):
    id = db.Column(db.INTEGER, unique=True, nullable=False, primary_key=True)
    sentFrom = db.Column(db.String(30), unique=False, nullable=False, primary_key=False)
    sentTo = db.Column(db.String(30), unique=False, nullable=False, primary_key=False)
    postId = db.Column(db.INTEGER, unique=False, nullable=False, primary_key=False)
    message = db.Column(db.String(300), unique=False, nullable=False, primary_key=False)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "sentFrom: {}".format(self.sentFrom)
        return "sentTo: {}".format(self.sentTo)
        return "postId: {}".format(self.postId)
        return "message: {}".format(self.message)

# index page
@app.route('/', methods=["GET", "POST"])
def index():
    path = "/var/www/sfsuListings/sfsuListings/"
    con = sqlite3.connect("postdatabase.db") # connects to the database
    con.row_factory = sqlite3.Row  # this creates rows for the sqlite? not too sure about this
    cur = con.cursor()
    cur.execute("select * from Posts order by date desc")
    result = cur.fetchmany(8)
    """
    l = [None] * 10  # this write the image filenames into a list, which is sent to results.html
    for row in result:
        j = row['id']
        i = row['id']
        l[j] = "item" + str(row['id']) + ".jpg"

        filename ='static/item' + str(i) + '.jpg'
        if (row['image'] != None):  # if the image is not null
            userImage = open(filename, 'wb')
            userImage.write(row[
                                'image'])  # this writes the image into a .jpg file, trying to figure out how to write into different extensions.
    """
    return render_template('HomePage.html', searchResult = result)###, list = l)
    
@app.route('/blueprint')
def pageBlueprint():
    #To query: tablename.query.filterby(column name= thing to be filtered by)
    postResults = Posts.query.filter_by(category="electronics")

    return render_template('blueprint.html', results=postResults)

    '''
    To add something to the db, first create the object 
    last = Posts.query.all()
    lastId = last[-1].id + 1;
    post = Posts(name = "example", author = "bob", id=lastId, price = 4, category = "example")
    db.session.add(post)
    db.session.commit()
    '''

@app.route('/logout')
def logout():
    '''
    Ends the users session and logs out the user.
    '''
    session['logged_in'] = False
    session['user_name'] = None
    return redirect('/')


@app.route('/IndividualPost/<post_id>')
def IndividualPost(post_id):
	post_id = post_id
	postResult = Posts.query.filter_by(id=post_id).first()
	return render_template('IndividualPost.html', post = postResult)
	

@app.route('/termsOfService')
def termsOfService():
    return render_template('termsOfService.html')

@app.route('/Dashboard')
def Dashboard():
    return render_template('Dashboard.html')

@app.route('/PostSearch')
def PostSearch():
    return render_template('PostSearch.html')

@app.route('/DashboardMessage')
def DashboardMessage():
    return render_template('DashboardMessage.html')

@app.route('/AdminDashboard')
def AdminDashboard():
    return render_template('AdminDashboard.html')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.debug = True  # Turn on auto reloader and debugger
    app.config['SQLALCHEMY_ECHO'] = True  # Show SQL commands created
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.run()
