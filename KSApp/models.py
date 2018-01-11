from KSApp import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(200))
    email = db.Column(db.String(256),unique=True)
    urole = db.Column(db.String(80))


    def __init__(self,username,password,email,urole):
            self.username = username
            self.password = password
            self.email = email
            self.urole = urole


    def get_id(self):
            return self.id
    def get_username(self):
            return self.username
    def get_urole(self):
            return self.urole





class Servers(db.Model):
    __tablename__ = 'servers'
    id = db.Column(db.Integer, primary_key=True)
    servername = db.Column(db.String(200), nullable=False, unique=True)
    ipaddress = db.Column(db.String(80), nullable=False)
    primaryrole = db.Column(db.String(200), nullable=False)
    secondaryrole = db.Column(db.String(200), nullable=True)
    commission = db.Column(db.Date, nullable=True)
    make = db.Column(db.String(100), nullable=True)
    serverinfo = relationship("serverinfo", uselist=False, backref="servers")
    serverdrives = relationship("serverdrives", uselist=False, backref="servers")

    def __init__(self, servername, ipaddress, primaryrole, secondaryrole, commission, make):

            self.servername = servername
            self.ipaddress = ipaddress
            self.primaryrole = primaryrole
            self.secondaryrole = secondaryrole
            self.commission = commission
            self.make = make

    def get_id(self):
            return self.id

    def get_servername(self):
            return self.servername

    def get_ipaddress(self):
        return self.ipaddress


class serverinfo(db.Model):
    __tablename__ = 'serverinfo'
    id = db.Column(db.Integer, primary_key=True)
    servers_id = db.Column(db.Integer, db.ForeignKey("servers.id"))
    operatingsystem = db.Column(db.String(200), nullable=True)
    cpuload = db.Column(db.Integer, nullable=True)
    totalram = db.Column(db.Integer, nullable=True)
    ramnotinuse = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(10))
    cpuname = db.Column(db.String(200))
    numofcores = db.Column(db.Integer)
    numofcpu = db.Column(db.Integer)


    def __init__(self, operatingsystem, drivemapping, drivefreespace,
                 drivetotalspace, cpuload, ramuseage, totalram, ramnotinuse, status, cpuname, numofcores, numofcpu):

        self.operatingsystem = operatingsystem
        self.drivemapping = drivemapping
        self.drivefreespace = drivefreespace
        self.drivetotalspace = drivetotalspace
        self.cpuload = cpuload
        self.ramuseage = ramuseage
        self.totalram = totalram
        self.ramuseage = ramnotinuse
        self.status = status
        self.cpuname = cpuname
        self.numofcores = numofcores
        self.numofcpu = numofcpu

    def get_id(self):
        return self.id



class serverdrives(db.Model):
    __tablename__ = "serverdrives"
    id = db.Column(db.Integer, primary_key=True)
    servers_id = db.Column(db.Integer, db.ForeignKey("servers.id"))
    drivemapping = db.Column(db.String(200), nullable=True)
    drivefreespace = db.Column(db.Integer, nullable=True)
    drivetotalspace = db.Column(db.Integer, nullable=True)





