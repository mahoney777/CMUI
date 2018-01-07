from KSApp import app, login_manager, db
from flask import render_template, flash, redirect, session, url_for, request, logging, sessions
from flask_bootstrap import Bootstrap
from functools import wraps
from KSApp.forms import RegisterForm, LoginForm, AddServerForm, ReusableForm, IPAddressform, add_domain_account
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from KSApp.models import Users, Servers, domainuser, serverinfo
from sqlalchemy import text
import wmi, os
from wmiutil import Connector
import threading


print("TEST")
i = Connector(None,None,None)
i.connect()



@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
@app.route('/index')
def homepage():
    return render_template('index.html', ip = "1", hdd = "2", used = "3", total = "4")#need to fix with wmi support


@app.route("/servers", methods=['GET', 'POST'])
def servers():
    #This is needed to get wmi to work
    form = ReusableForm()
    servernames = form.searchServer.data
    sdataname = ""
    osname = ""
    #this checks it exists
    #exists = db.session.query(db.exists().where(Servers.servername == servernames)).scalar()
    #print(exists)
    print(servernames)
    print("Test")
    #Trying to get SQLALC to search for the server in the webpage and print result....
    if servernames != None:
        #Getting WMI info
        p = Connector(None,None,None) #Change this to use the server info from the form
        osname = p.connect()
        stest = db.engine.execute(text("SELECT * FROM SERVERS WHERE servername = :servernames"), servernames=servernames)
        servern = []
        for row in stest:
            print(row)
            servern=row
            sdataname = servern


    return render_template('servers.html', form = form, sdataname = sdataname, osname = osname)



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

@app.route('/addserver', methods=['GET', 'POST'])
@login_required
def addserver():
    form = AddServerForm()

    if form.validate_on_submit():
        new_server = Servers(servername=form.servername.data, ipaddress=form.ipaddress.data,
                             primaryrole=form.primaryrole.data, secondaryrole=form.secondaryrole.data,
                             operatingsystem=form.operatingsystem.data, commission=form.commission.data,
                             make=form.make.data, num_cpu=form.num_cpu.data, cpu_model=form.cpu_model.data,
                             ram_gb=form.ram_gb.data, vm=form.vm.data)

        db.session.add(new_server)
        db.session.commit()
        return redirect(url_for('admin'))



    return render_template('addserver.html', form = form)


@app.route('/stats', methods=['GET','POST'])
@login_required
def stats():
    data=''
    form = IPAddressform()
    print(current_user)
    domainusername = db.engine.execute(text("""SELECT domainuser.domainusername AS Users FROM 
                                            domainuser INNER JOIN Users ON Users.id = domainuser.id 
                                            WHERE domainuser.id = 1"""))
    stuff = []
    for row in domainusername:
        print(row)
        stuff = row
        thedata = stuff
        print(thedata)
        info = thedata[0].split()
        duser = info[0]
        dpwd = DOMAIN_USER_PWD
        print(dpwd)


    if form.validate_on_submit():
        ip = form.ipaddress.data
        ipsearch = Connector(ip,duser,dpwd)
        data = ipsearch.connect()
        print(data)



    return render_template('stats.html', form = form, data=data)



@app.route('/domainaccount', methods=['GET','POST'])
@login_required
def domainaccount():
    form = add_domain_account()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_domain_user = domainuser(domainusername=form.username.data, domainpassword=hashed_password)
        db.session.add(new_domain_user)
        db.session.commit()
        #export password to env variable
    return render_template('domainaccount.html', form = form)





if __name__ == '__main__':
    KSApp.run(debug=True, use_reloader=True)