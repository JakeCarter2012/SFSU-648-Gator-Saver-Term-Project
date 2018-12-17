from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint, url_for
import sqlite3
import logging
import base64
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, DateTime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import  secure_filename
from pathlib import Path
import os

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

login = Flask(__name__)

db = SQLAlchemy(login)

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
    postTitle = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
    message = db.Column(db.String(300), unique=False, nullable=False, primary_key=False)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "sentFrom: {}".format(self.sentFrom)
        return "sentTo: {}".format(self.sentTo)
        return "postId: {}".format(self.postId)
        return "message: {}".format(self.message)


@dashboard.route('/Dashboard')
def dashboardRoute():
    return redirect('/Dashboard/Posts')


@dashboard.route('/Dashboard/')
def dashboardSlash():
    return redirect('/Dashboard/Posts')


@dashboard.route('/Dashboard/Posts')
def postDashboard():
    if ((session.get('logged_in') == None) or (session.get('logged_in') == False)):
        flash('Please log in before accessing your dashboard.')
        return redirect('/login')

    postResult = Posts.query.filter_by(author=session.get('user_name')).first()

    posts = Posts.query.filter_by(author=session.get('user_name'))
    messages = Messages.query.filter_by(sentTo=session.get('user_name'))
    errorString = {"string": 'You don\'t have any items posted yet. Want to post an item?',
                   "post": True}
    return render_template('Dashboard.html', QueryPosts=posts, QueryMessage=messages, post=postResult, eString=errorString)


@dashboard.route('/Dashboard/Posts/<post_id>')
def postDashboardId(post_id):
    post_id = post_id
    if ((session.get('logged_in') == None) or (session.get('logged_in') == False)):
        flash('Please log in before accessing your dashboard.')
        return redirect('/login')

    postResult = Posts.query.filter_by(id=post_id).first()

    if((postResult is None) or (postResult.author != session.get('user_name'))):
        return redirect('/Dashboard/Posts')


    posts = Posts.query.filter_by(author=session.get('user_name'))
    messages = Messages.query.filter_by(sentTo=session.get('user_name'))
    return render_template('Dashboard.html', QueryPosts=posts, QueryMessage=messages, post=postResult)


@dashboard.route('/Dashboard/Messages')
def messageDashboard():
    if ((session.get('logged_in') == None) or (session.get('logged_in') == False)):
        flash('Please log in before accessing your dashboard.')
        return redirect('/login')

    message = Messages.query.filter_by(sentTo=session.get('user_name')).first()

    id= message.postId
    title = message.postTitle
    sentFrom = message.sentFrom

    messageResults = Messages.query.filter_by(postId=id).filter(or_(Messages.sentFrom == sentFrom, Messages.sentTo == sentFrom))

    posts = Posts.query.filter_by(author=session.get('user_name'))
    messages = Messages.query.filter_by(sentTo=session.get('user_name'))
    errorString = {"string": 'You don\'t have any messages.'}
    return render_template('Dashboard.html', QueryPosts=posts, QueryMessage=messages,
                           messages=messageResults, eString=errorString, title=title)


@dashboard.route('/Dashboard/Messages/<message_id>')
def messageDashboardId(message_id):
    message_id = message_id
    if ((session.get('logged_in') == None) or (session.get('logged_in') == False)):
        flash('Please log in before accessing your dashboard.')
        return redirect('/login')

    message = Messages.query.filter_by(id=message_id).first()

    if ((message is None) or (message.sentTo != session.get('user_name'))):
        return redirect('/Dashboard/Messages')

    title = message.postTitle
    id = message.postId
    sentFrom = message.sentFrom

    messageResults = Messages.query.filter_by(postId=id).filter(or_(Messages.sentFrom == sentFrom, Messages.sentTo == sentFrom))

    posts = Posts.query.filter_by(author=session.get('user_name'))
    messages = Messages.query.filter_by(sentTo=session.get('user_name'))
    errorString = {"string": 'You don\'t have any messages.'}
    return render_template('Dashboard.html', QueryPosts=posts, QueryMessage=messages,
                           messages=messageResults, eString=errorString, title=title)


@dashboard.route('/Admin', methods=['GET'])
def adminLoginPage():
    return render_template('AdminLogin.html')


@dashboard.route('/Admin', methods=['POST'])
def adminLogin():
    admin = Admin.query.filter_by(AdminName=request.form['username']).first()
    if admin is None or not admin.check_password(request.form['password']):
        flash('Invalid username or password.')
        return redirect('/Admin')
    session['admin_logged_in'] = True
    return redirect('/Admin/Dashboard')

@dashboard.route('/Admin/Dashboard')
def AdminDashboard():
    if ((session.get('admin_logged_in') == None) or (session.get('admin_logged_in') == False)):
        flash('Employees must log in to review posts.')
        return redirect('/Admin')

    postResult = Posts.query.filter_by(approval='pending').first()

    posts = Posts.query.filter_by(approval='pending')
    errorString = {"string": 'All pending posts have been reviewed.'}
    return render_template('AdminDashboard.html', QueryPosts=posts, post=postResult, eString=errorString)


@dashboard.route('/Admin/logout')
def adminLogout():
  session['logged_in'] = False
  session['user_name'] = None
  return redirect('/Admin')

@dashboard.route('/Admin/Dashboard/<post_id>')
def AdminDashboardId(post_id):
    post_id = post_id
    if((session.get('admin_logged_in') == None) or (session.get('admin_logged_in') == False)):
        flash('Employees must log in to review posts.')
        return redirect('/Admin')

    postResult = Posts.query.filter_by(id=post_id).first()

    if (postResult is None):
        return redirect('/Admin/Dashboard')

    posts = Posts.query.filter_by(approval='pending')
    errorString = {"string": 'All pending posts have been reviewed.'}
    return render_template('AdminDashboard.html', QueryPosts=posts, post=postResult, eString=errorString)


@dashboard.route('/Admin/Review/<post_id>', methods=["POST"])
def AdminDashboardReview(post_id):
    post_id = post_id
    if((session.get('admin_logged_in') == None) or (session.get('admin_logged_in') == False)):
        flash('Employees must log in to review posts.')
        return redirect('/Admin')

    post = Posts.query.filter_by(id=post_id).first()
    post.approval = request.form['status']
    db.session.commit()

    if(post is None):
        return redirect('/Admin/Dashboard')

    return redirect('/Admin/Dashboard')
