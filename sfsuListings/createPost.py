from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint, url_for
import logging
import base64
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from werkzeug.utils import  secure_filename
from pathlib import Path
from sfsuListings.configPaths import image_path
import os

createPost = Blueprint('createPost', __name__, template_folder='templates')

UPLOAD_FOLDER = image_path
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

login = Flask(__name__)

db = SQLAlchemy(login)

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@createPost.route('/CreatePost', methods=['GET'])
def createPostGet():
    return render_template('CreatePost.html', title='Create Post')

@createPost.route('/CreatePost', methods=['POST'])
def createNewPost():
    if ((session.get('logged_in') == None) or (session.get('logged_in') == False)):
        flash('Please log in before creating a post.')
        return redirect('/login')
    title = request.form['title']
    category = request.form['category']
    price = request.form['price']
    description = request.form['description']
    last = Posts.query.all()
    lastId = last[-1].id + 1
    img = ''
    if('img' not in request.files):
        img = 'NoImageAvailable.png'
    else:
        image = request.files['img']
        if(image.filename == ''):
            img = 'NoImageAvailable.png'
        elif(image and allowed_file(image.filename)):
            imageName = secure_filename("Post_" + str(lastId) + Path(image.filename).suffix)
            image.save(os.path.join((UPLOAD_FOLDER), imageName))
            img = imageName
        else:
            img = 'NoImageAvailable.png'
    newPost = Posts(name=title, author=session.get('user_name'), price=price, category=category,
                    description=description, image=img, id=lastId, approval='Pending')
    db.session.add(newPost)
    db.session.commit()
    return redirect('/Dashboard')
