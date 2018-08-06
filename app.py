from flask import (Flask, render_template, flash, redirect,
                   url_for, session, logging, request, g, render_template_string)
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from flask_user import login_required, UserManager, UserMixin
from flask_pymongo import PyMongo


app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY']= 'super secret key 12344567891234'
# app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']


# Flask-MongoEngine settings
MONGODB_SETTINGS = {
    'db': 'sb-hoa',
    'host': 'mongodb://localhost:27017/sb-hoa'
}


db = MongoEngine(app)
# app.session_interface = MongoEngineSessionInterface(db)
# toolbar = DebugToolbarExtension(app)


# Flask-User settings
USER_APP_NAME = "Sea Breeze HOA"      # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form
USER_AFTER_LOGIN_ENDPOINT = 'index'

app.config.from_object(__name__)


# Define the User document.
# NB: Make sure to add flask_user UserMixin
class User(db.Document, UserMixin):
    active = db.BooleanField(default=True)

    # User authentication information
    username = db.StringField(default='')
    password = db.StringField()

    # User information
    first_name = db.StringField(default='')
    last_name = db.StringField(default='')
    email = db.StringField(default='')


    # Relationships
    roles = db.ListField(db.StringField(), default=[])


# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)


def cur_user_info():
    """used to return user info"""

    for cur_user in User.objects:
        cur_user = cur_user.username

    for cur_first_name in User.objects:
        cur_first_name = cur_first_name.first_name

    for cur_last_name in User.objects:
        cur_last_name = cur_last_name.last_name

    for cur_user_email in User.objects:
        cur_user_email = cur_user_email.email

    return cur_user, cur_first_name, cur_last_name, cur_user_email


# The Home page is accessible to anyone
@app.route('/')
def home_page():
    
    app.logger.debug('User.username type is {}'.format(type(User.username)))
    return render_template_string("""
        {% extends "flask_user_layout.html" %}
        {% block content %}
            <h2>Home page</h2>
            <p><a href={{ url_for('user.register') }}>Register</a></p>
            <p><a href={{ url_for('user.login') }}>Sign in</a></p>
            <p><a href={{ url_for('home_page') }}>Home page</a> (accessible to anyone)</p>
            <p><a href={{ url_for('index') }}>Member page</a> (login required)</p>
            <p><a href={{ url_for('user.logout') }}>Sign out</a></p>
        {% endblock %}
        """)


#Home
@app.route('/index')
@login_required
def index():

    for cur_user in User.objects:
        cur_user = cur_user.username

    return render_template('index.html', cur_user=cur_user)

# Announcements
@app.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():

	return render_template('announcements.html')

@app.route('/conference_room', methods=['GET', 'POST'])
@login_required
def conference_room():

	return render_template('conference_room.html')


@app.route('/account-settings', methods=['GET', 'POST'])
@login_required
def account_settings():

    cur_user, cur_first_name, cur_last_name, cur_user_email = cur_user_info()

    if request.method == 'POST':
        
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        User.objects(first_name=cur_first_name).update(first_name=first_name) # Update
        User.objects(last_name=cur_last_name).update(last_name=last_name)
        User.objects(email=cur_user_email).update(email=email)

        


    return render_template('account-settings.html', cur_first_name=cur_first_name, cur_last_name=cur_last_name, cur_user_email=cur_user_email)


if __name__ == '__main__':
    app.secret_key = 'super secret key 12344567891234'
    app.run(debug=True, port=1111, host='localhost')
