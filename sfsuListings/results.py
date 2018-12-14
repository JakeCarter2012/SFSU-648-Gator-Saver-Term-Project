from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint
import sqlite3
import logging
import base64
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
searchResults = Blueprint('searchResults', __name__, template_folder='templates')


@searchResults.route('/results', methods=["GET", "POST"])
def results():
    path = "/var/www/sfsuListings/sfsuListings/"
    con = sqlite3.connect("postdatabase.db") # connects to the database
    con.row_factory = sqlite3.Row  # this creates rows for the sqlite? not too sure about this
    cur = con.cursor()
    nameSearch = request.form["search"]  # gets data from search bar
    category = request.form["categories"] 
    if category != "All":
        cur.execute("select * from Posts where name like ? and category like ?",
                    (nameSearch + '%', category,))  # searches from posts table and matches search result to category
    else:    
        cur.execute("select * from Posts where category like ? ",
                    (nameSearch + '%',)) 
    result = cur.fetchall()            
    # filename to write blob info into
    '''
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
    '''
    return render_template('PostSearch.html', searchQuery=result, search=nameSearch)
    '''                         ,list=l)  # renders results.html, searchQuery is the list of items from database'''
