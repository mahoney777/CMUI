from wtforms import Form, StringField, TextAreaField, IntegerField, PasswordField, validators, DateField, RadioField


class RegisterForm(Form):
    username = StringField('Username', [validators.required(), validators.Length(min=4, max=30)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


"""class AddServerForm(Form):
    servername = StringField('Server Name', [validators.input_required(), validators.length(min=4, max=50)])
    ipaddress = StringField('IP Address', [validators.input_required(), validators.length(min=9, max=50)])
    primaryrole = StringField('Primary Role', [validators.input_required(), validators.length(min=2, max=100)])
    secondaryrole = StringField('Secondary Role', validators.length(min=4, max=100)])
    operatingsystem = StringField('OS', validators.input_required, validators.length(min=4, max=100)])
    commision = DateField("Commision Date",format="%Y-%b-%d",[validators.Optional()])
    make = StringField('Make (HP)'), validators.length(min=1, max=50)])
    num_cpu = IntegerField('Number of CPUs', validators.input_required(), validators.NumberRange(min=1, max=10)])
    cpu_model = StringField('CPU Model (use the exact model name)'), validators.input_required, validators.length(min=3,max=50)])
    ram_gb = IntegerField('Amount of RAM in GB', validators.input_required, validators.number_range(min=1,max=11)])
    vm = RadioField('Gender', choices = [(1,'is VM'),(0,'is not VM'), validators.required()])
"""