import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class emailer():
    """Emailer to send notifications"""

    def __init__(self, receiver, sender, subject, body):
        self.receiver = receiver
        self.sender = sender
        self.subject = subject
        self.body = body

    def emailsender(self, receiver, sender, subject, body, exchangeserver):
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()
        # print text
        # Send the message via our SMTP server
        s = smtplib.SMTP('our.exchangeserver.com')
        s.sendmail(sender, receiver, text)
        s.quit()