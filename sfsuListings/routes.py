from sfsuListings import app, db
from sfsuListings.models import Posts, Messages, Admin
from flask import render_template, flash, redirect, url_for, request, session
import sqlite3
import logging



# index page
@app.route('/index')
@app.route('/')
def index():
    result = Posts.query.filter_by(approval='approved')
    result = result.order_by(Posts.date.desc())
    return render_template('HomePage.html', searchResult=result, title="Home") 


@app.route('/images/<image>')
def images(image):
    image = image
    imgPath = os.path.join('images', image)
    return send_file(imgPath)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_name'] = None
    return redirect('/')


@app.route('/IndividualPost/<post_id>')
def IndividualPost(post_id):
    post_id = post_id
    postResult = Posts.query.filter_by(id=post_id).first()
    postName = postResult.name
    return render_template('IndividualPost.html', post=postResult, title=postName)

@app.route('/IndividualPost/<post_id>', methods = ['POST'])
def addMessage(post_id):
  if session.get('logged_in') == None or session.get('logged_in') == False:
    flash('Please log in before sending a message.')
    return redirect('/login')
  messageBody = request.form['subject']
  currentUser = session.get('user_name')
  postResult = Posts.query.filter_by(id=post_id).first()
  postName = postResult.name
  newMessage = Messages(sentFrom = currentUser, sentTo = postResult.author, postId = postResult.id, postTitle = postResult.name, message = messageBody)  
  db.session.add(newMessage)
  db.session.commit()
  flash('Your message has been sent.')
  return render_template('IndividualPost.html', title=postName, post=postResult)

@app.route('/IndividualPost/')
def IndividualPostBad():
  return redirect('/')


@app.route('/termsOfService')
def termsOfService():
    tosTitle = 'Terms of Service'
    return render_template('termsOfService.html', title=tosTitle)


@app.route('/PostSearch')
def PostSearch():
    return render_template('PostSearch.html', title='Search')


@app.route('/AdminDashboard')
def AdminDashboard():
    return render_template('AdminDashboard.html', title='Admin Dashboard')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
