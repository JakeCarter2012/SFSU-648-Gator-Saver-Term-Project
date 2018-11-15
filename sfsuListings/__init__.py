
import logging
import base64

import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, request, session, abort, g

from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os

from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

database_file = "sqlite:///postdatabase.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

migrate = Migrate(app,db)
#NOTE: Secret key resets to new key each time server is restarted;
#this will invalidate any old session cookies the user has, and requires log out
#can hardcode the secret key to 'solve' this, but is considered unsafe practice
app.config['SECRET_KEY'] = os.urandom(24)


#model class
class Posts(db.Model):
    name = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)
    author = db.Column(db.String(80), unique=False, nullable=True, primary_key=True)
    id = db.Column(db.INTEGER, unique=True, nullable=False, primary_key=False ,autoincrement=True)
    price = db.Column(db.INTEGER, unique=False, nullable=False, primary_key=True)
    image = db.Column(db.BLOB, unique = False,nullable = True,primary_key=False)
    category = db.Column(db.String(80),unique = False, nullable = False, primary_key = False)

    def __repr__(self):
        return "<Name: {}>".format(self.name)
        return "<Author: {}".format(self.author)
        return "<id: {}".format(self.id)
        return "<price: {}".format(self.price)
        return "<image: {}".format(self.image)
        return "<category: {}".format(self.category)
'''    
Class for registered user; note that passord is hashed
to compare passwords the check_password fuction must be called
'''
class RegisteredUser(db.Model):
    UserName = db.Column(db.String(30), unique=True, nullable=False, primary_key=True)
    password_hash = db.Column(db.String(96), unique=True, nullable=False, primary_key=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<Username: {}>".format(self.UserName)
        return "<Hashed Password: {}".format(self.password_hash)

#index page
@app.route('/', methods = ["GET","POST"])
def index():
    return render_template('HomePage.html')


@app.route('/results',methods = ["GET","POST"])
def results():
   path = "/var/www/sfsuListings/sfsuListings/"
   con = sqlite3.connect(path + "postdatabase.db") #connects to the database 
   con.row_factory = sqlite3.Row # this creates rows for the sqlite? not too sure about this
   cur = con.cursor() 
   search = request.form["search"] #gets data from search bar
   cur.execute("select * from Posts where category like ?", (search+'%',)) #searches from posts table and matches search result to category
   result = cur.fetchall() #retrieves list of queried items and stores it in result
    #filename to write blob info into
   l = [None] * 10 #this write the image filenames into a list, which is sent to results.html
   for row in result: 
    j = row['id'] 
    i = row['id']
    l[j] = "item" + str(row['id']) + ".jpg"
    
    filename = path + 'static/item' + str(i) +'.jpg'
    if(row['image'] != None): #if the image is not null
        userImage = open(filename ,'wb')
        userImage.write(row['image']) # this writes the image into a .jpg file, trying to figure out how to write into different extensions.
           
   return render_template('results.html',searchQuery = result, search = search, list = l) #renders results.html, searchQuery is the list of items from database

   
#sub pages
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
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

@app.route('/SignUp' , methods=['GET'])
def SignUp():
    return render_template('SignUp.html')	

@app.route('/SignUp' , methods=['POST'])
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
                             password_hash=generate_password_hash(request.form['password']))
    db.session.add(newUser)
    db.session.commit()
    session['logged_in'] = True
    session['user_name'] = request.form['username']
    return redirect('/')

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

#about page 
@app.route('/about')    
def about():
    return render_template('about.html')

@app.route('/jake')
def jake():
    return render_template('aboutJake.html')

@app.route('/gary')
def gary():
    return render_template('garyd.html')

@app.route('/martin')
def martin():
    return render_template('MartinLeeAboutPage.html')

@app.route('/wagner')
def wagner():
    return render_template('WagnerAbout.html')

@app.route('/gordon')
def gordon():
    return render_template('Gordon about page.html')

@app.route('/tina')
def tina():
    return render_template('About Tina.html')

@app.route('/alvin')
def alvin():
    return render_template('aboutAlvin.html')

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

