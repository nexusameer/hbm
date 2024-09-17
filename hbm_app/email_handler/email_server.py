import smtplib
import hbm_app.python_scripts.hbm_api as hbm_api
import re
import os
from datetime import datetime

def incoming_email_credentials(admin=False):
    if admin:
        keys = {
            'credentials': (os.getenv('ADMIN_CLIENT_ID'), os.getenv('ADMIN_CLIENT_SECRET')),
            'tenant': os.getenv('ADMIN_TENANT_ID'),
            'sender_email': os.getenv('ADMIN_INCOMING_EMAIL_ADDRESS'),
        }
    else:
        keys = {
            'credentials': (os.getenv('CLIENT_ID'), os.getenv('CLIENT_SECRET')),
            'tenant': os.getenv('CLIENT_TENANT_ID'),
            'sender_email': os.getenv('CLIENT_EMAIL_ADDRESS'),
        }
    return keys

def outgoing_email_credentials():
    keys = {
        'smtp_server': os.getenv('ADMIN_EMAIL_SERVER'),
        'port': os.getenv('ADMIN_EMAIL_PORT'),
        'sender_email': os.getenv('ADMIN_OUTGOING_EMAIL_ADDRESS'),
        'password': os.getenv('ADMIN_EMAIL_PASSWORD')
    }
    return keys


def init_email_server():
    print('\nStarting Email server....')
    email = outgoing_email_credentials()
    global server
    try:
        try: 
            server = smtplib.SMTP_SSL(email.get('smtp_server'), email.get('port'))
        except smtplib.ssl.SSLError:
            server = smtplib.SMTP(email.get('smtp_server'),  email.get('port'))
            server.ehlo()
            server.starttls() 
        server.login(email.get('sender_email'), email.get('password'))
    except smtplib.socket.gaierror:
        print('ERROR: Mail server does not exist.')
    except ConnectionRefusedError:
        print('ERROR: SMTP port is incorrect.')
    except smtplib.SMTPServerDisconnected:
        print('ERROR: Email login credentials are incorrect.') 

    print('Server started...')
    return email.get('sender_email')


def msg_generator(sender_email, receiver_email, subject, message, files=None, cc=None, bcc=None):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.application import MIMEApplication
    from os.path import basename
    msg = MIMEMultipart()
    msg['From'] = f"Data HBM <{sender_email}>"
    msg['To'] = ", ".join(receiver_email)
    if cc:
        msg['Cc'] = ", ".join(cc)
    if bcc: 
        msg['Bcc'] = ", ".join(bcc)

    msg['Subject'] = subject

    # Reply to address
    msg.add_header('reply-to', 'data@hoornbloommasters.com')
    msg.attach(MIMEText(message, 'html'))

    for f in files or []:
        with open(f, "r") as attachment_file:
            part = MIMEApplication(
                attachment_file.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
    return msg


def send_email(sender_email, receivers, msg, email_text=None):
    # Filter out None emails
    receivers = [i for i in receivers if i is not None]

    server.sendmail(sender_email, receivers, msg.as_string())
    for receiver in receivers:
        print('Email sent to ' + receiver)


def close_server():
    print('Closing email server...')
    server.quit()