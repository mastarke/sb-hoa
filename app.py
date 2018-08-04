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



app = Flask(__name__)

app.config['MONGO_HOST'] = 'mastarke-lnx-v2'
app.config['MONGO_DBNAME'] = 'meritDB'

# INIT MONGODB
mongo = PyMongo(app)


# INDEX
@app.route('/', methods=['GET', 'POST'])
def index():

	return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True, port=1111, host='localhost')
