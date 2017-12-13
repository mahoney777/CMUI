from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, EqualTo



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50), ])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password')

"""
class AddServerForm(FlaskForm):
    servername = StringField('Server Name', [validators.input_required(), validators.length(min=4, max=50)])
    ipaddress = StringField('IP Address', [validators.input_required(), validators.length(min=9, max=50)])
    primaryrole = StringField('Primary Role', [validators.input_required(), validators.length(min=2, max=100)])
    secondaryrole = StringField('Secondary Role', [validators.length(min=4, max=100)])
    operatingsystem = StringField('OS', [validators.input_required, validators.length(min=4, max=100)])
    commission = DateField("Commission Date", format="%Y-%b-%d")
    make = StringField('Make (HP)', [validators.length(min=1, max=50)])
    num_cpu = IntegerField('Number of CPUs', [validators.input_required(), validators.NumberRange(min=1, max=10)])
    cpu_model = StringField('CPU Model (use the exact model name)', [validators.input_required, validators.length(min=3,max=50)])
    ram_gb = IntegerField('Amount of RAM in GB', [validators.input_required, validators.number_range(min=1,max=11)])
    vm = RadioField('VM', choices = [(1,'is VM'),(0,'is not VM'), validators.required()])
"""