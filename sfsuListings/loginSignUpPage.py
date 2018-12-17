import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os


from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

database_file = "sqlite:///postdatabase.db"

loginSignUpPage = Blueprint('loginSignUpPage', __name__, template_folder='templates')

login = Flask(__name__)

db = SQLAlchemy(login)

'''    
Class for registered user; note that password is hashed
to compare passwords the check_password fuction must be called
'''
class RegisteredUser(db.Model):
    UserName = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    password_hash = db.Column(db.String(96), unique=False, nullable=False, primary_key=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + 'sfsu')

    def __repr__(self):
        return "<Username: {}>".format(self.UserName)
        return "<Hashed Password: {}".format(self.password_hash)



# sub pages
@loginSignUpPage.route('/login', methods=['GET'])
def login():
    return render_template('login.html', title='Login')


@loginSignUpPage.route('/login', methods=['POST'])
def login_submit():
    '''
    Post method for login submission; query's database for entered username,
    If username doesn't exist, or the password doesn't match the hatched password,
    return an error to the user, otherwise log the user's session in.
    '''
    user = RegisteredUser.query.filter_by(UserName=request.form['username']).first()
    if user is None or not user.check_password(request.form['password']):
        flash('Invalid username or password.')
        return redirect('/login')
    session['logged_in'] = True
    session['user_name'] = request.form['username']
    return redirect('/')

@loginSignUpPage.route('/SignUp', methods=['GET'])
def SignUp():
    return render_template('SignUp.html', title='Register')


@loginSignUpPage.route('/SignUp', methods=['POST'])
def register():
    '''
    Queries the database to see if the username is taken; then compares passwords to ensure they are the same.
    If either check fails, the user is flashed with the error. Otherwise, the user's account
    is created and their password is hashed, and they are logged in as their new account name.

    For captcha localhost testing, use:
    Site key: 6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI
    captchakey: 6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe
    use the site key in SignUp.html
    '''
    user = RegisteredUser.query.filter_by(UserName=request.form['username']).first()
    missingField = False
    if user is not None:
        flash('User name is already taken.')
        missingField = True
    if request.form['password'] != request.form['repassword']:
        flash('Passwords do not match.')
        missingField = True
    if request.form.get('termsCheckBox') == None:
        flash('Please accept the terms and conditions of use.')
        missingField = True
    if request.form.get('g-recaptcha-response') == "" or request.form.get('g-recaptcha-response') == None:
        flash('Captcha invalid')
        missingField = True
    else:
        '''
        Captcha validation: Send request to google api with our domain's key
        and the captcha's output; then receive json and parse it to see
        if captcha was passed or not
        '''
        captchaKey = '6Ldu6noUAAAAAKQTCQMVOj5_IfZR6XaKPVFzNJmx'
        post_fields = {'secret': captchaKey,
                       'response': request.form.get('g-recaptcha-response')}
        url = 'https://www.google.com/recaptcha/api/siteverify'
        captchaRequest = Request(url, urlencode(post_fields).encode())
        jsonRaw = urlopen(captchaRequest).read().decode()
        jsonData = json.loads(jsonRaw)
        if jsonData['success'] == False:
            flash('Captcha failed - are you sure you are not a robot?')
            missingField = True

    if missingField:
        return redirect('/SignUp')

    newUser = RegisteredUser(UserName=request.form['username'],
                             password_hash=generate_password_hash(request.form['password'] + 'sfsu'))
    db.session.add(newUser)
    db.session.commit()
    session['logged_in'] = True
    session['user_name'] = request.form['username']
    return redirect('/')
    #To see if a user is logged/ get their username: use session['logged_in'] and session['user_name']
