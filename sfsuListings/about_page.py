from flask import Flask, flash, redirect, render_template, request, session, abort, g, Blueprint
about_page = Blueprint('about_page', __name__, template_folder='templates')

# about page
@about_page.route('/about')
def about():
    return render_template('about.html')


@about_page.route('/about_page.jake')
def jake():
    return render_template('aboutJake.html')


@about_page.route('/abut_page.gary')
def gary():
    return render_template('garyd.html')


@about_page.route('/about_page.martin')
def martin():
    return render_template('MartinLeeAboutPage.html')


@about_page.route('/about_page.wagner')
def wagner():
    return render_template('WagnerAbout.html')


@about_page.route('/about_page.gordon')
def gordon():
    return render_template('Gordon about page.html')


@about_page.route('/about_page.tina')
def tina():
    return render_template('About Tina.html')


@about_page.route('/about_page.alvin')
def alvin():
    return render_template('aboutAlvin.html')
