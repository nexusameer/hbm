from imapclient import IMAPClient
import mailparser

print('hello')
CLIENT_EMAIL_SERVER="smtp.office365.com"
# CLIENT_EMAIL_SERVER="outlook.office365.com"
# CLIENT_EMAIL_PORT=587
# CLIENT_EMAIL_ADDRESS="adnansheikh681@outlook.com"
# CLIENT_EMAIL_PASSWORD="Bitf13a501"
# CLIENT_EMAIL_ADDRESS="data@hoornbloommasters.com"
# CLIENT_EMAIL_PASSWORD="Fak56203"
CLIENT_EMAIL_ADDRESS="adnan@wegmetexcel.nl"
CLIENT_EMAIL_PASSWORD="977d218a-530b-4a41-88ed-07611f1cabfd"
# CLIENT_EMAIL_PASSWORD="Pakistan1824"
# #data@hoornbloommasters.com



from O365 import Account

credentials = ('ccea2919-4301-4c12-a30f-e73dfd608239', 'XxB8Q~kaI6t6LsDGHjeMQnnBBH_-PH5CMXGvtbNP')

# the default protocol will be Microsoft Graph

account = Account(credentials, auth_flow_type='credentials', tenant_id='52400cca-c161-4c38-afcb-cda0cd301e98')
import pdb; pdb.set_trace()
if account.authenticate():
   print('Authenticated!')
mailbox = account.mailbox(resource=CLIENT_EMAIL_ADDRESS)
inbox = mailbox.inbox_folder()
query = inbox.q().on_attribute('from').equals('sheikhadnan133@gmail.com')
for message in inbox.get_messages(query=query, download_attachments=True):
   if message.has_attachments:
      for attachment in message.attachments:
         import os
         from pathlib import Path
         BASE_DIR = Path(__file__).resolve().parent.parent
         attachment.save(os.path.join(BASE_DIR, 'data_input'))
         print(attachment)
      message.move('Archive')
   print(message)


# from exchangelib import Credentials, Account
# # credentials = ('ccea2919-4301-4c12-a30f-e73dfd608239', '977d218a-530b-4a41-88ed-07611f1cabfd')
# import pdb; pdb.set_trace()
# credentials = Credentials('ccea2919-4301-4c12-a30f-e73dfd608239', '977d218a-530b-4a41-88ed-07611f1cabfd')

# account = Account(CLIENT_EMAIL_ADDRESS, credentials=credentials, autodiscover=True)

# for item in account.inbox.all().order_by('-datetime_received')[:100]:
#     print(item.subject, item.sender, item.datetime_received)

# with IMAPClient(CLIENT_EMAIL_SERVER) as server:
#     print(server.welcome)
#     print(CLIENT_EMAIL_ADDRESS)
#     server.oauth2_login(CLIENT_EMAIL_ADDRESS, CLIENT_EMAIL_PASSWORD)
#     server.select_folder('INBOX')
#     messages = server.search(['UNSEEN', ])  # in your case: ['FROM', 'email@outlook.example']

#     # for each unseen email in the inbox
#     for uid, message_data in server.fetch(messages, 'RFC822').items():
#         email_message = mailparser.parse_from_string(message_data[b'RFC822'])