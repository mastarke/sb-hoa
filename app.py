from flask import (Flask, render_template, flash, redirect,
                   url_for, session, logging, request, g, render_template_string)
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_debugtoolbar import DebugToolbarExtension
from flask_user import login_required, UserManager, UserMixin, current_user
import datetime
from mongoengine.context_managers import switch_collection
import json


app = Flask(__name__)
# app.debug = True

app.config['SECRET_KEY']= 'super secret key for me123456789987654321'
# app.config['DEBUG_TB_PANELS'] = ['flask_mongoengine.panels.MongoDebugPanel']


app.config['MONGODB_SETTINGS'] = {
    'db': 'sb-hoa',
    'host': 'mongodb://localhost:27017/sb-hoa',
    # 'host':'mongodb://mastarke:cisco123@ds215502.mlab.com:15502/sb-hoa'
}


db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)
toolbar = DebugToolbarExtension(app)


# Flask-User settings
USER_APP_NAME = "Sea Breeze HOA"      # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = True    # Simplify register form
USER_AFTER_LOGIN_ENDPOINT = 'index'
USER_ENABLE_REMEMBER_ME = False
USER_AUTO_LOGIN = False

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

    profile_pic = db.FileField(default='')

    # Relationships
    roles = db.ListField(db.StringField(), default=[])

class Announcement(db.Document):
    title = db.StringField(max_length=60)
    text = db.StringField()
    done = db.BooleanField(default=False)
    pub_date = db.DateTimeField(default=datetime.datetime.now())
    username = db.StringField(default='')



# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)


def cur_user_info():
    """used to return user info"""

    cur_user = current_user.username

    for cur_first_name in User.objects:
        cur_first_name = cur_first_name.first_name

    for cur_last_name in User.objects:
        cur_last_name = cur_last_name.last_name

    for cur_user_email in User.objects:
        cur_user_email = cur_user_email.email

    return cur_user, cur_first_name, cur_last_name, cur_user_email


def get_post_info():

    num_post = Announcement.objects.count()
    print('matthew num_post is {}'.format(num_post))
    print('matthew num_post type is {}'.format(type(num_post)))

    # msg title info from db
    msg_title_list = []
    for msg_title in Announcement.objects.order_by('-pub_date'):
        msg_title = msg_title.title
        msg_title_list.append(msg_title)
        
    
    # get msg text from db
    msg_text_list = []
    for msg_text in Announcement.objects.order_by('-pub_date'):
        msg_text = msg_text.text
        msg_text_list.append(msg_text)

    # get msg date from db
    pub_date_list = []
    for pub_date in Announcement.objects.order_by('-pub_date'):
        pub_date = pub_date.pub_date
        pub_date_list.append(pub_date)
    
    # get username from db
    user_name_list = []
    for username in Announcement.objects.order_by('-pub_date'):
        username = username.username
        user_name_list.append(username)


    # get username from db
    msg_id_list = []
    for msg_id in Announcement.objects.order_by('-pub_date'):
        msg_id = msg_id.id
        msg_id_list.append(msg_id)



    # This returns <class 'mongoengine.queryset.queryset.QuerySet'>
    
    q_set = Announcement.objects.order_by('-pub_date')
    json_data = q_set.to_json()

    # You might also find it useful to create python dictionaries
    post_dict = json.loads(json_data)

    for num in range(num_post):
        print('######## this is number {} ###########'.format(num))
        for key, value in post_dict[num].items():
            if key == 'username':
                print('key is {} value is {}'.format(key, value))
            elif key == 'pub_date':
                print('key is {} value is {}'.format(key, value))
            elif key == 'title':
                print('key is {} value is {}'.format(key, value))
            elif key == 'text':
                print('key is {} value is {}'.format(key, value))


        print('######## END OF ITEM {} ###########'.format(num))


    


    return msg_title_list, msg_text_list, pub_date_list, user_name_list, post_dict, num_post

# The Home page is accessible to anyone
@app.route('/')
def home_page():
    
    
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

    cur_user = current_user.username

    cur_user_id = current_user.id
    

    return render_template('index.html', cur_user=cur_user)

# emergency contacts
@app.route('/emergency-contacts')
@login_required
def emergency_contacts():

    return render_template('emergency-contacts.html')


# budget
@app.route('/budget')
@login_required
def budget():

    return render_template('budget.html')

    

# Announcements
@app.route('/announcements', methods=['GET', 'POST'])
@login_required
def announcements():
    
    cur_user = current_user.username

    msg_title_list, msg_text_list, pub_date_list, user_name_list, post_dict, num_post = get_post_info()

    print('Matthew your in announcements and num_post is {}'.format(num_post))
    print('%%%%%% Matthew your in announcements and post_dict is {} %%%%%%%%'.format(post_dict[0]))

    return render_template('announcements.html', cur_user=cur_user, 
                                                 post_dict=post_dict, 
                                                 num_post=num_post, 
                                                 msg_data=zip(msg_title_list, 
                                                              msg_text_list, 
                                                              pub_date_list,
                                                              user_name_list))

# Announcements
@app.route('/post_announcements', methods=['GET', 'POST'])
@login_required
def post_announcements():

    cur_user = current_user.username

    if request.method == 'POST':

        # get form data
        message_title = request.form['message_title']
        message_text = request.form['message_text']

        # push msg info into db
        Announcement(username=cur_user, title=message_title, text=message_text).save()

    return render_template('post_announcements.html')


# Announcements
@app.route('/edit_announcements', methods=['GET', 'POST'])
@login_required
def edit_announcements():

    
    return render_template('edit_announcements.html')

        

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


        profile_pic = request.form['profile_pic']
        app.logger.debug('Matthew you have profile_pic'.format(type(profile_pic)))
        # User.profile_pic.put(marmot_photo, content_type = 'image/jpeg')

        
    return render_template('account-settings.html', cur_first_name=cur_first_name, cur_last_name=cur_last_name, cur_user_email=cur_user_email)


if __name__ == '__main__':
    app.secret_key = 'super secret key for me123456789987654321'
    app.run(debug=True, port=1111, host='localhost')
