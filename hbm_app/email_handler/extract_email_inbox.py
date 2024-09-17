import os
import hbm_app.email_handler.email_server as email_server
from pathlib import Path
from O365 import Account


def imap_server():
    global account
    global email
    
    # Get credentials 
    email = email_server.incoming_email_credentials()
    # the default protocol will be Microsoft Graph
    account = Account(email.get('credentials'), auth_flow_type='credentials', tenant_id=email.get('tenant'))
    account.authenticate()


def read_inbox(action, from_email_address, customer_name=None):
    imap_server()
    BASE_DIR = Path(__file__).resolve().parent.parent
    mailbox = account.mailbox(resource=email.get('sender_email'))
    # Select inbox
    inbox = mailbox.inbox_folder()
    email_attachment_list = []
    senders = list(map(str.strip, from_email_address.split(',')))
    for sender in senders: 
        query = inbox.q().on_attribute('from').contains(sender)
        for message in inbox.get_messages(query=query, download_attachments=True):
            attachment_list = []
            print(from_email_address)
            if message.has_attachments:
                for attachment in message.attachments:
                    _, file_extension = os.path.splitext(attachment.name)
                    if file_extension in ['.csv', '.xlsx', '.xls']:  
                        dir_path = os.path.join(BASE_DIR, 'data_input')
                        file_name = str(message.sent.date()) + " - " + customer_name + " - " + attachment.name
                        file_path = os.path.join(dir_path, file_name)
                        print(file_name)
                        if not os.path.exists(file_path):
                            attachment.save(location=dir_path, custom_name=file_name)
                            attachment_list.append(file_path)
                email_attachment_list.append({'email': message, 'attachments': attachment_list})
    return email_attachment_list


def move_email_to_archive(action, email):
    if not action.test:
        email.move('Archive')

    