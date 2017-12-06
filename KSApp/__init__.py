import os
from flask import Flask
from volumecap import Harddrive
from filter import getsevername
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mahoney'
app.config['MYSQL_PASSWORD'] = 'Yb1dAI3vna3xTAMuJNOV'
app.config['MYSQL_DB'] = 'ksdb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


address = getsevername()
hdd = Harddrive
drive, freeSpace, totalSpace = hdd.diskspace(None)

from KSApp import views,forms