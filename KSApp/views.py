from KSApp import app, login_manager, db
from flask import render_template, flash, redirect, session, url_for, request, logging, sessions
from flask_bootstrap import Bootstrap
from functools import wraps
from KSApp.forms import RegisterForm, LoginForm, AddServerForm, ReusableForm, IPAddressform, add_domain_account
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from KSApp.models import Users, Servers, serverinfo, serverdrives
from sqlalchemy import text
import wmi, os
from wmiutil import Connector
import threading
from itertools import chain
import time
import schedule


def reloadserverstats():
    serverIP = []
    x = os.environ.get("DOMAIN_USERNAME")
    y = os.environ.get("DOMAIN_PWD")
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


def emailer():



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
    return Users.query.get(int(user_id))

@app.route('/')
@app.route('/welcome')
def homepage():
    return render_template('index.html')#need to fix with wmi support


@app.route("/servers", methods=['GET', 'POST'])
def servers():
    drivelists = []
    testlist = []
    print("""
        
        
        
        
        
    """)
    ##########################################
    """I need to create a system where
    data from the database can be passed
    as different servers- stuff in testfile"""
    ##########################################

    test = db.engine.execute(text("""SELECT servers.id, servers.servername, servers.primaryrole, servers.secondaryrole, 
            serverinfo.cpuname, serverinfo.operatingsystem FROM servers LEFT JOIN serverinfo 
            ON serverinfo.servers_id = servers.id GROUP BY servers.id"""))

    drives = db.engine.execute(text("""SELECT serverdrives.servers_id, serverdrives.drivemapping, serverdrives.drivefreespace, 
            serverdrives.drivetotalspace, serverdrives.percentused FROM serverdrives"""))


    for row in test:
        testlist.append({'Server ID': row[0], 'ServerName': row[1], 'Primary Role': row[2], 'Secondary Role': row[3],
                         'CPU-Name': row[4], 'Operating System': row[5]})

    for row in drives:
        drivelists.append({'Server ID': row[0], 'Drive Mapping': row[1], 'FreeSpace': row[2], 'TotalSpace': row[3],
                           'Percentage Used': row[4]})






    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")
    print(testlist)
    print("-----------------------------------------------------------------------")
    print(drivelists)
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")


    return render_template('servers.html', basicserverinfo=testlist, serverdrives = drivelists)


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
@login_required
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Users(username=form.username.data, email=form.email.data, password=hashed_password, urole="user")
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login.html'))

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
        print(x, y)
        z = form.ipaddress.data

        server_info = Connector(z, x, y)

        #get varibles
        #
        # allstats = server_info.allstats()
        #
        vm, name, status, operatingsystem, notinuse, totalmem, \
        numofcores, numofcpu, cpuname, avgcpuload, uptime, drivelist = server_info.allstats()
        print(vm, name, status, numofcpu, numofcores)

        new_server = Servers(servername=form.servername.data, ipaddress=form.ipaddress.data,
                             primaryrole=form.primaryrole.data, secondaryrole=form.secondaryrole.data,
                             commission=form.commission.data, make=form.make.data)

        db.session.add(new_server)
        db.session.commit()

        ipadd = db.engine.execute(text("SELECT id FROM SERVERS WHERE ipaddress = :IPA"), IPA=form.ipaddress.data)
        for row in ipadd:
            print(row)
            serverid = row[0]
            print(serverid)

        new_serverinfo = serverinfo(servers_id = serverid, operatingsystem=operatingsystem, cpuload=avgcpuload,
                                    ramnotinuse=notinuse, totalram=totalmem, status=status,
                                    cpuname=cpuname, numofcores=numofcores, numofcpu=numofcpu)

        db.session.add(new_serverinfo)
        db.session.commit()

        drivelistlen = len(drivelist)

        for i in range(drivelistlen):
            mapping, totalspace, freespace, percentageused = drivelist[i]
            print(mapping, freespace, totalspace)

            new_serverdrives = serverdrives(servers_id = serverid, drivemapping=mapping, drivefreespace = freespace,
                                           drivetotalspace = totalspace, percentused=percentageused)

            db.session.add(new_serverdrives)
            db.session.commit()

        return redirect(url_for('admin'))



    return render_template('addserver.html', form = form)


@app.route('/stats', methods=['GET', 'POST'])
@login_required
def stats():
    form = IPAddressform()
    x = os.environ.get("DOMAIN_USERNAME")
    y = os.environ.get("DOMAIN_PWD")

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



@app.route('/domainaccount', methods=['GET','POST'])
@login_required
def domainaccount():
    form = add_domain_account()

    if form.validate_on_submit():
        os.environ["DOMAIN_USERNAME"] = form.username.data
        #could make hashing/encryting/decryt this
        os.environ["DOMAIN_PWD"] = form.password.data
        #export password to env variable
        print(os.environ.get('DOMAIN_USERNAME'))
        print(os.environ.get('DOMAIN_PWD'))
    return render_template('domainaccount.html', form = form)





if __name__ == '__main__':
    KSApp.run(debug=True, use_reloader=True)
    #####schedule.every(10).minutes.do(reloadserverstats())