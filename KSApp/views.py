from KSApp import app,address,drive,freeSpace,totalSpace, login_manager, db
from flask import render_template, flash, redirect, session, url_for, request, logging
from flask_bootstrap import Bootstrap
from functools import wraps
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def homepage():
    return render_template('index.html', ip = address, hdd = drive, used = freeSpace, total = totalSpace)


@app.route('/servers')
def servers():
    return render_template('servers.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admin'))


        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password, urole="user")
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/addserver')
@login_required
def addserver():
    return render_template('addserver.html')



if __name__ == '__main__':
    KSApp.run(debug=True, use_reloader=True)