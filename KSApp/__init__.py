import os
from volumecap import Harddrive
from filter import getsevername
from flask_mysqldb import MySQL
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, redirect, session, url_for, request, logging
from functools import wraps
from .forms import RegisterForm
from passlib.hash import sha256_crypt
from flask.ext.security import current_user, login_required, RoleMixin, Security, SQLAlchemyUserDatastore, UserMixin, utils


app = Flask(__name__)
app.config.from_object('config')



#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'mahoney'
#app.config['MYSQL_PASSWORD'] = 'Yb1dAI3vna3xTAMuJNOV'
#app.config['MYSQL_DB'] = 'ksdb'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#mysql = MySQL(app)

app.config['SQLAlchemy_DATABASE_URI'] = 'mysql://mahoney:Yb1dAI3vna3xTAMuJNOV@127.0.0.1:3306/ksdb2'

db = SQLAlchemy(app)

address = getsevername()
hdd = Harddrive
drive, freeSpace, totalSpace = hdd.diskspace(None)

from KSApp import views,forms