from flask import (Flask, render_template, flash, redirect,
                   url_for, session, logging, request, g)
from flask_pymongo import PyMongo
import pymongo
from collections import OrderedDict
import re
import os
import uuid
import datetime
import sys
import bcrypt



app = Flask(__name__)

app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_DBNAME'] = 'sb-hoa'

# INIT MONGODB
mongo = PyMongo(app)


# INDEX
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('register'))

    return render_template('index.html')

# Announcements
@app.route('/announcements', methods=['GET', 'POST'])
def announcements():

	return render_template('announcements.html')

@app.route('/conference_room', methods=['GET', 'POST'])
def conference_room():

	return render_template('conference_room.html')




@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')





@app.route('/utility-account-settings', methods=['GET', 'POST'])
def utility_account_settings():

	return render_template('utility-account-settings.html')




if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, port=1111, host='localhost')
