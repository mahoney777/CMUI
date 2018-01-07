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
    domainuser = relationship('domainuser', uselist=False, back_populates="users")



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


class domainuser(db.Model):
    __tablename__ = 'domainuser'
    id = db.Column(db.Integer, primary_key=True)
    domainusername = db.Column(db.String(200))
    domainpassword = db.Column(db.String(200))
    users_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    users = relationship("Users", back_populates="domainuser")

    def __int__(self,id,domainusername, domainpassword):
        self.id = id
        self.domainusername = domainuser
        self.domainpassword = domainpassword

    def get_id(self):
        return self.id



class Servers(db.Model):
    __tablename__ = 'Servers'
    id = db.Column(db.Integer, primary_key=True)
    servername = db.Column(db.String(200), nullable=False, unique=True)
    ipaddress = db.Column(db.String(80), nullable=False)
    primaryrole = db.Column(db.String(200), nullable=False)
    secondaryrole = db.Column(db.String(200), nullable=True)
    operatingsystem = db.Column(db.String(200), nullable=False)
    commission = db.Column(db.Date, nullable=True)
    make = db.Column(db.String(100), nullable=True)
    num_cpu = db.Column(db.Integer, nullable=False)
    cpu_model = db.Column(db.String(80), nullable=False)
    ram_gb = db.Column(db.Integer, nullable=False)
    vm = db.Column(db.Boolean, default=False)

    def __init__(self,servername,ipaddress,primaryrole,secondaryrole,
                 operatingsystem, commission, make, num_cpu, cpu_model, ram_gb, vm):

            self.servername = servername
            self.ipaddress = ipaddress
            self.primaryrole = primaryrole
            self.secondaryrole = secondaryrole
            self.operatingsystem = operatingsystem
            self.commission = commission
            self.make = make
            self.num_cpu = num_cpu
            self.cpu_model = cpu_model
            self.ram_gb = ram_gb
            self.vm = vm

    def get_id(self):
            return self.id

    def get_servername(self):
            return self.servername

    def get_ipaddress(self):
        return self.ipaddress


class serverinfo(db.Model):
    __tablename__ = 'serverinfo'
    id = db.Column(db.Integer, primary_key=True)
    operatingsystem = db.Column(db.String(200), nullable=True)
    #need to change this if there is more than one drive in the server
    drivemapping = db.Column(db.String(200), nullable=True)
    drivefreespace = db.Column(db.Integer, nullable=True)
    drivetotalspace = db.Column(db.Integer, nullable=True)
    cpuload = db.Column(db.Integer, nullable=True)
    ramuseage = db.Column(db.Integer, nullable=True)
    totalram = db.Column(db.Integer, nullable=True)
    ramnotinuse = db.Column(db.Integer, nullable=True)


    def __init__(self, id, operatingsystem, drivemapping, drivefreespace,
                 drivetotalspace, cpuload, ramuseage, totalram, ramnotinuse):

        self.id = id
        self.operatingsystem = operatingsystem
        self.drivemapping = drivemapping
        self.drivefreespace = drivefreespace
        self.drivetotalspace = drivetotalspace
        self.cpuload = cpuload
        self.ramuseage = ramuseage
        self.totalram = totalram
        self.ramuseage = ramnotinuse

    def get_id(self):
        return self.id







