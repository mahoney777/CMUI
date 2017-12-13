from KSApp import db
from flask_login import UserMixin

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

"""
class Servers(db.Model):
    __tablename__ = 'Servers'
    id = db.Column(db.Integer, primary_key=True)
    servername = db.Column(db.String(200), nullable=False)
    ipaddress = db.Column(db.String(80), nullable=False)
    primaryrole = db.Column(db.String(200), nullable=False)
    secondaryrole = db.Column(db.String(200), nullable=True)
    operatingsystem = db.Column(db.String(200), nullable=False)
    commission = db.Column(db.String(100), nullable=True)
    make = db.Column(db.String(200), nullable=True)
    num_cpu = db.Column(db.Integer(10), nullable=False)
    cpu_model = db.Column(db.String, nullable=False)
    ram_gb = db.Column(db.Integer(10), nullable=False)
    vm = db.Column(db.Boolean, default=False)
"""
