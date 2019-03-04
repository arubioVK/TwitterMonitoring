
from flask_mail import Mail, Message
from app.__init__ import dameEmail
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

mail=dameEmail()

def enviarEmail(asunto, cuerpo, destinatario):
    msg = Message(asunto, sender = 'XXX@gmail.com', recipients = [destinatario])
    msg.body = cuerpo
    mail.send(msg)

def enviarEmailBorradoTweet(toaddr, subject, body):
    fromaddr = "XXX@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()



