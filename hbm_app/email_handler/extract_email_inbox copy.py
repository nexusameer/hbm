import imaplib
import os
import email as email_lib
import hbm_app.email_handler.email_server as email_server
from pathlib import Path


def imap_server():
    global imap
    # Get credentials 
    email = email_server.email_credentials()
    # Setup imap and login with credentials.
    imap = imaplib.IMAP4_SSL(email.get('smtp_server'), 993)
    imap.login(email.get('sender_email'), email.get('password'))


def close_imap_server():
    # close the connection and logout
    imap.close()
    imap.logout()


def read_inbox(action, from_email_address):
    imap_server()

    # Select inbox
    imap.select("inbox")

    # Filter on emails in the inbox folder if they are from sender.
    result, selected_mails = imap.uid('search', None, f'(FROM {from_email_address})')
    selected_mails = selected_mails[0].split()
    email_attachment_list = []
    # Loop over emails. 
    for num in selected_mails:
        _, data = imap.uid('fetch', num, '(RFC822)')
        _, bytes_data = data[0]

        # Convert the byte data to message
        email_message = email_lib.message_from_bytes(bytes_data)

        print(f"Date: {email_message['date']} Subject: {email_message['subject']}")
        datetime_obj = email_lib.utils.parsedate_to_datetime(email_message["date"])

        attachment_list = []
        # Get attachment out of email. 
        for part in email_message.walk():
            fileName = part.get_filename()
            # Check if there is a filename, and if it is an xls or xlsx file 
            if bool(fileName):
                if fileName.endswith('.xls') or fileName.endswith('.xlsx'):
                    # Save Attachment
                    BASE_DIR = Path(__file__).resolve().parent.parent
                    version = 0
                    # If file already exists in data input folder, you want to prevent overwriting it. Therefore a _Version will be added to every file whose name already exists, to create a unique name. 
                    while True:
                        if version == 0:
                            fileNameMod = datetime_obj.strftime("%Y%m%d-%H%M%S") + ' ' + fileName
                        else:
                            fileNameMod = datetime_obj.strftime("%Y%m%d-%H%M%S") + '_' + str(version) + ' ' + fileName
                        filePath = os.path.join(BASE_DIR, 'data_input', fileNameMod)
                        if not os.path.isfile(filePath):
                            fp = open(filePath, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
                            break
                        else:
                            version = version + 1
                    # Append to attachment list, that will later be used to handle all new files. 
                    attachment_list.append(filePath)
        email_attachment_list.append({'email': num, 'attachments': attachment_list})       

    return email_attachment_list


def move_email_to_archive(action, num):
    if not action.test:
        # Move email to Archief only if the run isn't test.
        result = imap.uid('COPY', num, 'Archief')
        # Delete email in inbox folder. 
        if result[0] == 'OK':
            mov, data = imap.uid('STORE', num , '+FLAGS', '(\Deleted)')
            imap.expunge()


    