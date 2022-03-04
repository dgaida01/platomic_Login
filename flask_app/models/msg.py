from flask_mail import Mail, Message
from flask_app import app, session

app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = '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'
app.config['MAIL_DEFAULT_SENDER'] = 'platomic.info@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
# app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

class AutoCom:
    def __init__(self):
        self.subject = 'hello'

    @classmethod
    def sendMessage(cls, subject,to, body):
        msg = Message(subject,recipients=[to],sender='platomic.info@gmail.com')
        msg.html = body
        mail.send(msg)
    
