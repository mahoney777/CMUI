from KSApp import *
from flask import request, render_template, flash, redirect, url_for, Blueprint, g
from flask_login import current_user, login_user, logout_user, login_required
from KSApp.models import User

dashboard = Blueprint('dashboard', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@dashboard.before_request
def get_current_user():
    g.user = current_user

@dashboard.route('/admin')
def admin():
    return render_template('admin.html')

@dashboard.route('/addserver')
def addserver():
    return render_template('addserver.html')

