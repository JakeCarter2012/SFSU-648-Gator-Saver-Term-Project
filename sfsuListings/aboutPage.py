from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint
aboutPage = Blueprint('about_page', __name__, template_folder='templates')

# about page
@aboutPage.route('/about')
def about():
    return render_template('about.html')


@aboutPage.route('/aboutPage.jake')
def jake():
    return render_template('aboutJake.html')


@aboutPage.route('/aboutPage.gary')
def gary():
    return render_template('garyd.html')


@aboutPage.route('/aboutPage.martin')
def martin():
    return render_template('MartinLeeAboutPage.html')


@aboutPage.route('/aboutPage.wagner')
def wagner():
    return render_template('WagnerAbout.html')


@aboutPage.route('/aboutPage.gordon')
def gordon():
    return render_template('Gordon about page.html')


@aboutPage.route('/aboutPage.tina')
def tina():
    return render_template('About Tina.html')


@aboutPage.route('/aboutPage.alvin')
def alvin():
    return render_template('aboutAlvin.html')
