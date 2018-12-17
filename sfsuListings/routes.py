from sfsuListings import app, db
from sfsuListings.models import Posts, Messages, Admin
from flask import render_template, flash, redirect, url_for, request
import sqlite3

# index page
@app.route('/', methods=["GET", "POST"])
def index():
    path = "/var/www/sfsuListings/sfsuListings/"
    con = sqlite3.connect("postdatabase.db")  # connects to the database
    con.row_factory = sqlite3.Row  # this creates rows for the sqlite? not too sure about this
    cur = con.cursor()
    cur.execute("select * from Posts order by date desc")
    result = cur.fetchmany(8)
    return render_template('HomePage.html', searchResult=result)  ###, list = l)


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

    return render_template('IndividualPost.html', post=postResult)

@app.route('/IndividualPost/')
def IndividualPostBad():
  return redirect('/')


@app.route('/termsOfService')
def termsOfService():
    return render_template('termsOfService.html')


@app.route('/PostSearch')
def PostSearch():
    return render_template('PostSearch.html')


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