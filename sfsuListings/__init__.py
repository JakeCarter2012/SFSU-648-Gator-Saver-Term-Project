import logging
import base64

import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint

from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os

from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from aboutPage import aboutPage
from loginSignUpPage import loginSignUpPage

database_file = "sqlite:///postdatabase.db"

app = Flask(__name__)

app.register_blueprint(aboutPage)
app.register_blueprint(loginSignUpPage)

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
    author = db.Column(db.String(80), unique=False, nullable=True, primary_key=True)
    id = db.Column(db.INTEGER, unique=True, nullable=False, primary_key=False, autoincrement=True)
    price = db.Column(db.INTEGER, unique=False, nullable=False, primary_key=True)
    image = db.Column(db.BLOB, unique=False, nullable=True, primary_key=False)
    category = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)

    def __repr__(self):
        return "<Name: {}>".format(self.name)
        return "<Author: {}".format(self.author)
        return "<id: {}".format(self.id)
        return "<price: {}".format(self.price)
        return "<image: {}".format(self.image)
        return "<category: {}".format(self.category)


'''    
Class for registered user; note that password is hashed
to compare passwords the check_password fuction must be called
'''



# index page
@app.route('/', methods=["GET", "POST"])
def index():
    path = "/var/www/sfsuListings/sfsuListings/"
    con = sqlite3.connect("postdatabase.db") # connects to the database
    con.row_factory = sqlite3.Row  # this creates rows for the sqlite? not too sure about this
    cur = con.cursor()
    cur.execute("select * from Posts where category like ?",
                ('%',))
    result = cur.fetchmany(4)
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

    return render_template('HomePage.html', searchResult = result, list = l)
    

@app.route('/results', methods=["GET", "POST"])
def results():
    path = "/var/www/sfsuListings/sfsuListings/"
    con = sqlite3.connect("postdatabase.db") # connects to the database
    con.row_factory = sqlite3.Row  # this creates rows for the sqlite? not too sure about this
    cur = con.cursor()
    search = request.form["search"]  # gets data from search bar
    cur.execute("select * from Posts where category like ?",
                (search + '%',))  # searches from posts table and matches search result to category
    result = cur.fetchall()  # retrieves list of queried items and stores it in result
    # filename to write blob info into
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

    return render_template('PostSearch.html', searchQuery=result, search=search,
                           list=l)  # renders results.html, searchQuery is the list of items from database



@app.route('/logout')
def logout():
    '''
    Ends the users session and logs out the user.
    '''
    session['logged_in'] = False
    session['user_name'] = None
    return redirect('/')


@app.route('/IndividualPost')
def IndividualPost():
    return render_template('IndividualPost.html')


@app.route('/CreatePost')
def CreatePost():
    return render_template('CreatePost.html')


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

