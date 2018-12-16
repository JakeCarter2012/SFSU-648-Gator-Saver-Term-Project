from flask import Flask, url_for, flash, redirect, render_template, request, session, abort, g, Blueprint
aboutPage = Blueprint('about_page', __name__, template_folder='templates')

# about page
@aboutPage.route('/about')
def about():
    return render_template('about/about.html')


@aboutPage.route('/aboutPage.jake')
def jake():
    return render_template('about/jake.html')


@aboutPage.route('/aboutPage.gary')
def gary():
    return render_template('about/gary.html')


@aboutPage.route('/aboutPage.martin')
def martin():
    return render_template('about/martin.html')


@aboutPage.route('/aboutPage.wagner')
def wagner():
    return render_template('about/wagner.html')


@aboutPage.route('/aboutPage.gordon')
def gordon():
    return render_template('about/gordon.html')


@aboutPage.route('/aboutPage.tina')
def tina():
    return render_template('about/tina.html')


@aboutPage.route('/aboutPage.alvin')
def alvin():
    return render_template('about/alvin.html')
