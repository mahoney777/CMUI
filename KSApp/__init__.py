from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .forms import RegisterForm

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from KSApp.homemenu.views import homemenu
from KSApp.dashboard.views import dashboard



app.register_blueprint(homemenu)
app.register_blueprint(dashboard)


db.create_all()