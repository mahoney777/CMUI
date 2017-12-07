from volumecap import Harddrive
from filter import getsevername
#from .forms import RegisterForm
#from passlib.hash import sha256_crypt
import ldap
from flask import request, render_template, flash, redirect, url_for, Blueprint, g
from flask_login import current_user, login_user, logout_user, login_required
from KSApp import login_manager, db
from KSApp.models import User, LoginForm

homemenu = Blueprint('homemenu', __name__)
address = getsevername()
hdd = Harddrive
drive, freeSpace, totalSpace = hdd.diskspace(None)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@homemenu.before_request
def get_current_user():
    g.user = current_user


@homemenu.route('/')
@homemenu.route('/index')
def homepage():
    return render_template('.index.html', ip = address, hdd = drive, used = freeSpace, total = totalSpace)

@homemenu.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        flash('You are already logged in.')
        return redirect(url_for('.index'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('.login', form=form)

        user = User.query.filter_by(username=username).first()

        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('.index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('.login', form=form)


@homemenu.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.index'))

@homemenu.route('/servers')
def servers():
    return render_template('.servers.html')
