import os

SQLALCHEMY_DATABASE_URI = 'mysql://mahoney:Yb1dAI3vna3xTAMuJNOV@localhost:3306/ksdb2'
WTF_CSRF_SECRET_KEY = 'random key for form'
LDAP_PROVIDER_URL = 'ldap://ldap.testathon.net:389/'
LDAP_PROTOCOL_VERSION = 3


os.environ["DOMAIN_USERNAME"] = "CMUIAdmin"
os.environ["DOMAIN_PWD"] = "Admin2017"


DEBUG = True
CSRF_ENABLED = True
WTF_CSRF_ENABLED = True
SECRET_KEY = 'Yb1dAI3vna3xTAMuJNOV'

ADMINS = ['info@cmui.co.uk']