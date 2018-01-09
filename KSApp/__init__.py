import os
from flask import Flask
from filter import getsevername
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap



app = Flask(__name__)
app.config.from_object('config')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mahoney:Yb1dAI3vna3xTAMuJNOV@localhost:3306/testdb'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'hfoafoafodnpnad'
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please Login'



from .models import Users, Servers

db.create_all()
db.session.commit()

from KSApp import views