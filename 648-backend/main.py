
import logging

from flask import Flask, flash, redirect, render_template, request, session, abort


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

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

    app.run(host='127.0.0.1', port=8080,)

