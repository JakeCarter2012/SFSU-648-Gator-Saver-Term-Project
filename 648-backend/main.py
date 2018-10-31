
import logging
import base64

import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, render_template, request, session, abort, g

database_file = "sqlite:///postdatabase.db"

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

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



#index page
@app.route('/', methods = ["GET","POST"])
def index():

    return render_template('index.html')


@app.route('/results',methods = ["GET","POST"])
def results():
   con = sqlite3.connect("postdatabase.db") #connects to the database 
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
    
    filename = 'static/item' + str(i) +'.jpg'
    if(row['image'] != None): #if the image is not null
        userImage = open(filename ,'wb')
        userImage.write(row['image']) # this writes the image into a .jpg file, trying to figure out how to write into different extensions.
           
   return render_template('results.html',searchQuery = result, search = search, list = l) #renders results.html, searchQuery is the list of items from database

   
#sub pages
@app.route('/login')    
def login():
    return render_template('login.html')

@app.route('/SignUp')    
def SignUp():
    return render_template('SignUp.html')	

@app.route('/IndividualPost')    
def IndividualPost():
    return render_template('IndividualPost.html')	

@app.route('/CreatePost')    
def CreatePost():
    return render_template('CreatePost.html')	

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

