import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template


def emailer():
    fromaddr = "cmuiemailer@gmail.com"
    toaddr = "info@cmui.co.uk"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Test mail"

    body = "CMUI test"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "Zebra100")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()




def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    print(names, emails)
    return names, emails


get_contacts('contacts.txt')