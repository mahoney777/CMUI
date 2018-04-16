from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo, number_range, Optional



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50), ])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80),
                                                     EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')



class AddServerForm(FlaskForm):
    servername = StringField('Server Name', validators=[InputRequired(), Length(min=2, max=80)])
    ipaddress = StringField('IP Address', validators=[InputRequired(), Length(min=4, max=80)])
    primaryrole = StringField('Primary Role', validators=[InputRequired(), Length(min=1, max=200)])
    secondaryrole = StringField('Secondary Role', validators=[Length(min=1, max=200),Optional()])
    commission = DateField("Commission Date", format='%d/%m/%Y', validators=[Optional()])
    make = StringField('Manufacturer (HP)', validators=[InputRequired(), Length(min=1, max=100)])



class ReusableForm(FlaskForm):
    searchServer = StringField('Server:', validators=[InputRequired()])

class IPAddressform(FlaskForm):
    ipaddress = StringField("IP Address", validators=[])

class add_domain_account(FlaskForm):
    username = StringField('Domain Username', validators=[InputRequired(), Length(min=4, max=80)])
    password = PasswordField('Domain password', validators=[InputRequired(), Length(min=8, max=80),
                                                     EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

class emailform(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=3, max=80)])
    emailAddress = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50), ])

class emailremoveform(FlaskForm):
    emailAddress = StringField('Email Address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50), ])
