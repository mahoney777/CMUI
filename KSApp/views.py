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


def reloadserverstats():
    #reload the stats
    pass


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
@app.route('/index')
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

    test = db.engine.execute(text("""SELECT servers.servername, servers.primaryrole, servers.secondaryrole, 
            serverinfo.cpuname, serverinfo.operatingsystem FROM servers LEFT JOIN serverinfo 
            ON serverinfo.servers_id = servers.id GROUP BY servers.servername"""))

    drives = db.engine.execute(text("""SELECT serverdrives.drivemapping, serverdrives.drivefreespace, 
            serverdrives.drivetotalspace FROM serverdrives RIGHT JOIN servers ON servers_id = servers.id 
            WHERE servers_id = servers.id;"""))


    print(test)
    for row in test:
        testlist.append({'ServerName': row[0], 'Primary Role': row[1], 'Seconary Role': row[2], 'CPU-Name': row[3],
                         'Operating System': row[4]})


    for row in drives:
        drivelists.append({'Drive Mapping': row[0], 'FreeSpace': row[1], 'TotalSpace': row[2]})


    print("-----------------------------------------------------------------------")
    print(testlist)
    print()
    print(drivelists)


    return render_template('servers.html', basicserverinfo=testlist)


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
            mapping, totalspace, freespace = drivelist[i]
            print(mapping, freespace, totalspace)

            new_serverdrives = serverdrives(servers_id = serverid, drivemapping=mapping, drivefreespace = freespace,
                                           drivetotalspace = totalspace)

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
        ipsearch = Connector(ip,x,y)
        operatingsystem = ipsearch.connect()
        diskspace = ipsearch.diskspace()
        map = diskspace[0]
        free = diskspace[1]
        total = diskspace[2]
        uptime = ipsearch.get_uptime()
        cpuload = ipsearch.get_cpu()
        memory = ipsearch.totaltestmem()
        memorynotinuse = ipsearch.notinusemem()
        system = ipsearch.sysinfo()
        vm = system[0]
        name = system[1]
        status = system[2]

        return render_template('stats.html', form=form, os=operatingsystem, map = map,
                               free=free, total=total, uptime=uptime, cpu=cpuload,
                               mem=memory, notinuse=memorynotinuse, vm=vm, name=name,
                               status= status)

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