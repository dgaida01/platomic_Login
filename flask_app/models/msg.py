from flask_mail import Mail, Message
from flask_app import app, session

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'PlatomicAdm@outlook.com'
app.config['MAIL_PASSWORD'] = 'PbyD&A2021'
app.config['MAIL_DEFAULT_SENDER'] = 'PlatomicAdm@outlook.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

class AutoCom:
    def __init__(self):
        self.subject = 'hello'

    @classmethod
    def sendMessage(cls, subject,to, body):
        msg = Message(subject,recipients=[to],sender='PlatomicAdm@outlook.com')
        msg.html = body
        mail.send(msg)
    
