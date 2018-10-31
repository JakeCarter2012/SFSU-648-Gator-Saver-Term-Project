
import logging

from flask import Flask, flash, redirect, render_template, request, session, abort, url_for


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('HomePage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/SignUp')
def SignUp():
    return render_template('SignUp.html')






@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)
