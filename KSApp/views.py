from KSApp import app, login_manager, db
from flask import render_template, flash, redirect, session, url_for, request, logging, sessions
from flask_bootstrap import Bootstrap
from functools import wraps
from KSApp.forms import RegisterForm, LoginForm, AddServerForm, ReusableForm, IPAddressform, add_domain_account, emailform, emailremoveform
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from KSApp.models import Users, Servers, serverinfo, serverdrives
from sqlalchemy import text, exc
import wmi, os
from wmiutil import Connector
import threading
from itertools import chain
import time, string, random
import schedule
from VernamCipher import vc


encryption_key = "fwkbfkwbifwbbw828"

@app.before_first_request
def createAdminAccount():
    try:
        print("Checking for Admin account...")
        pw = ''.join(random.sample((string.ascii_uppercase + string.digits), 9))
        hashed_password = generate_password_hash(pw, method='sha256')
        new_user = Users(username='Admin', email='Admin@cmui.co.uk', password=hashed_password, urole="Admin")
        db.session.add(new_user)
        db.session.commit()
        print("------------------")
        print("New Admin account generated")
        print("Username = Admin, Password = "+pw)
        print("Check CMUI-Login.txt for details")
        print("------------------")
        f = open("CMUI-Login.txt", "w+")
        f.write("Username = Admin   Password = %s" % pw)
        f.close()
    except:
        print("Admin account exists")





def reloadserverstats():
    serverIP = []
    x = os.environ.get("DOMAIN_USERNAME")
    y = os.environ.get("DOMAIN_PWD")
    v = vc(y, encryption_key)
    y = v.VernamCipher(y, encryption_key)
    print(x, y)

    servers = db.engine.execute(text("""SELECT ipaddress FROM servers"""))

    #runtime needs to be added
    for ip in servers:
        serverIP.append(ip)
        reloader = Connector(ip, x, y)
        vm, name, status, operatingsystem, notinuse, totalmem, \
        numofcores, numofcpu, cpuname, avgcpuload, uptime, drivelist = reloader.allstats()
        drivelistlen = len(drivelist)
        for i in range(drivelistlen):
            mapping, totalspace, freespace, percentageused = drivelist[i]

        db.engine.execute(text("""UPDATE serverinfo SET serverinfo.operatingsystem = :OS, serverinfo.ramnotinuse = 
        :notinuse, serverinfo.totalram = :totalmem, serverinfo.numofcores = :cores, serverinfo.numofcpu = :cpu,
        serverinfo.cpuname = :cpuname, serverinfo.cpuload = :cpuload WHERE servers_id IN 
        (SELECT servers.id FROM servers WHERE ipaddress = :ip);"""))
        db.engine.execute(text("""UPDATE serverdrives SET serverdrives.drivemapping = :map, serverdrives.drivetotalspace,
        serverdrives.drivefreespace WHERE servers_id IN (SELECT servers.id FROM servers WHERE ipaddress = :ip); """))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@login_manager.user_loader
def load_user(user_id):
    try:
        return Users.query.get(int(user_id))
    except exc.InvalidRequestError:
        print("Error...")




@app.route('/')
@app.route('/welcome')
def homepage():
    return render_template('index.html')#need to fix with wmi support


@app.route("/servers", methods=['GET', 'POST'])
def servers():
    drivelists = []
    serverlist = []
    server = db.engine.execute(text("""SELECT servers.id, servers.servername, servers.primaryrole, servers.secondaryrole, 
            serverinfo.cpuname, serverinfo.operatingsystem FROM servers LEFT JOIN serverinfo 
            ON serverinfo.servers_id = servers.id GROUP BY servers.id"""))

    drives = db.engine.execute(text("""SELECT serverdrives.servers_id, serverdrives.drivemapping, serverdrives.drivefreespace, 
            serverdrives.drivetotalspace, serverdrives.percentused FROM serverdrives"""))


    for row in server:
        serverlist.append({'Server ID': row[0], 'ServerName': row[1], 'Primary Role': row[2], 'Secondary Role': row[3],
                         'CPU-Name': row[4], 'Operating System': row[5]})

    for row in drives:
        drivelists.append({'Server ID': row[0], 'Drive Mapping': row[1], 'FreeSpace': row[2], 'TotalSpace': row[3],
                           'Percentage Used': row[4]})

    return render_template('servers.html', basicserverinfo=serverlist, serverdrives = drivelists)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('admin'))

        flash('Wrong username or password')
        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password, urole="user")
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

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
        x = os.environ.get("DOMAIN_USERNAME")
        y = os.environ.get("DOMAIN_PWD")
        v = vc(y, encryption_key)
        y = v.VernamCipher(y, encryption_key)
        z = form.ipaddress.data
        server_info = Connector(z, x, y)
        vm, name, status, operatingsystem, notinuse, totalmem, \
        numofcores, numofcpu, cpuname, avgcpuload, uptime, drivelist = server_info.allstats()

        new_server = Servers(servername=form.servername.data, ipaddress=form.ipaddress.data,
                             primaryrole=form.primaryrole.data, secondaryrole=form.secondaryrole.data,
                             commission=form.commission.data, make=form.make.data)
        db.session.add(new_server)
        print("Adding Basics")
        time.sleep(2)
        db.session.commit()
        print("Added!")
        time.sleep(0.5)
        ipselect = db.engine.execute(text("SELECT id FROM SERVERS WHERE ipaddress = :IPA"), IPA=form.ipaddress.data)
        for row in ipselect:
            print(row)
            serverid = row[0]
        new_serverinfo = serverinfo(servers_id=serverid, operatingsystem=operatingsystem, cpuload=avgcpuload,
                                    ramnotinuse=notinuse, totalram=totalmem, status=status,
                                    cpuname=cpuname, numofcores=numofcores, numofcpu=numofcpu, uptime=uptime)
        db.session.add(new_serverinfo)
        print("Adding info...")
        time.sleep(2)
        db.session.commit()
        print("Added!")

        drivelistlen = len(drivelist)
        for i in range(drivelistlen):
            mapping, totalspace, freespace, percentageused = drivelist[i]
            new_serverdrives = serverdrives(servers_id = serverid, drivemapping=mapping, drivefreespace = freespace,
                                           drivetotalspace = totalspace, percentused=percentageused)
            db.session.add(new_serverdrives)
            db.session.commit()

        return redirect(url_for('admin'))

    return render_template('addserver.html', form = form)



######################################################
@app.route('/emailer', methods=['GET', 'POST'])
@login_required
def emailer():

    contactlist = []

    emailaddform = emailform()
    emailremoverform = emailremoveform()

    if request.method == 'GET':
        f = open("contacts.txt", "r")
        for line in f:
            contactlist.append(line)
        print(contactlist)

    if request.method == 'POST' and emailaddform.validate_on_submit():
        name = emailaddform.name.data
        emailaddress = emailaddform.emailAddress.data
        f = open('contacts.txt', 'a')
        f.write(name +' - '+ emailaddress +' \n')
        f.close()
        return redirect(url_for('emailer'))

    if request.method == 'POST' and emailremoverform.validate_on_submit():
        removeaddress = emailremoverform.emailAddress.data
        print(removeaddress)
        f = open('contacts.txt', 'r')
        lines = f.readlines()
        f.close()
        f = open('contacts.txt', 'w')
        for line in lines:
            if removeaddress not in line:
                f.write(line)
        f.close()
        return redirect(url_for('emailer'))



    return render_template('emailer.html', addform=emailaddform, removeform=emailremoverform, contactlist=contactlist)
#########################################################



@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    form = IPAddressform()
    x = os.environ.get("DOMAIN_USERNAME")
    y = os.environ.get("DOMAIN_PWD")
    print(y)

    v = vc(y, encryption_key)
    y = v.VernamCipher(y ,encryption_key)
    if form.validate_on_submit():
        ip = form.ipaddress.data
        connection = Connector(ip,x,y)
        vm, name, status, operatingsystem, notinuse, totalmem, \
        numofcores, numofcpu, cpuname, avgcpuload, uptime, drivelist = connection.allstats()
        drivelistlen = len(drivelist)
        for i in range(drivelistlen):
            mapping, totalspace, freespace, percentageused = drivelist[i]

            return render_template('stats.html', form=form, os=operatingsystem, map = mapping,
                                   free=freespace, total=totalspace, uptime=uptime, cpu=avgcpuload,
                                   mem=totalmem, notinuse=notinuse, vm=vm, name=name,
                                   status=status)

    return render_template('stats.html', form = form)


####################################################################
@app.route('/domainaccount', methods=['GET','POST'])
@login_required
def domainaccount():
    form = add_domain_account()

    if form.validate_on_submit():
        v = vc(form.password.data, encryption_key)
        y = v.VernamCipher(form.password.data, encryption_key)
        os.environ["DOMAIN_USERNAME"] = form.username.data
        os.environ["DOMAIN_PWD"] = y
        #export password to env variable
        print(os.environ.get('DOMAIN_USERNAME'))
        print(os.environ.get('DOMAIN_PWD'))
    return render_template('domainaccount.html', form = form)
#####################################################################




if __name__ == '__main__':
    KSApp.run(debug=True, use_reloader=True)

#THIS SHOULD WORK NEED TO TEST ON NETWORK#schedule.every(10).minutes.do(reloadserverstats())