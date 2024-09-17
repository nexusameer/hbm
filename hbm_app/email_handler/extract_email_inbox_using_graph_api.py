import os, base64
from pathlib import Path
import requests
from requests.auth import AuthBase
from msal import ConfidentialClientApplication, SerializableTokenCache
import hbm_app.email_handler.email_server as email_server
from hbm_app.models import Attachment, Customer
from django.utils import timezone

email = email_server.incoming_email_credentials(admin=True)

CLIENT_ID = email.get('credentials', ('', ''))[0]
CLIENT_SECRET = email.get('credentials', ('', ''))[1]
TENANT_ID = email.get('tenant')
CLIENT_EMAIL = email.get('sender_email')

class AuthProvider(AuthBase):
    def __init__(self, client_id, client_secret, tenant_id):
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.token_endpoint = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        self.token = self._get_token()

    def _get_token(self):
        app = ConfidentialClientApplication(
            self.client_id,
            authority=f'https://login.microsoftonline.com/{self.tenant_id}',
            client_credential=self.client_secret,
        )
        token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        return token_response['access_token']

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.token}'
        return r

def read_inbox(action, from_email_address, customer_name=None):
    BASE_DIR = Path(__file__).resolve().parent.parent
    endpoint = f'https://graph.microsoft.com/v1.0/users/{CLIENT_EMAIL}/mailFolders/Inbox/messages'
    auth_provider = AuthProvider(CLIENT_ID, CLIENT_SECRET, TENANT_ID)

    email_attachment_list = []
    senders = list(map(str.strip, from_email_address.split(',')))

    for sender in senders:
        params = {
            '$filter': f"contains(from/emailAddress/address, '{sender}')",
            '$expand': 'attachments',
        }
        response = requests.get(endpoint, params=params, auth=auth_provider)

        if response.status_code == 200:
            messages = response.json().get('value', [])
            for message in messages:
                attachment_list = []

                if 'attachments' in message:
                    for attachment in message['attachments']:
                        _, file_extension = os.path.splitext(attachment['name'])
                        if file_extension in ['.csv', '.xlsx', '.xls', '.xml']:
                            dir_path = os.path.join(BASE_DIR, 'data_input')
                            file_name = f"{message['sentDateTime']} - {customer_name} - {attachment['name']}"
                            file_path = os.path.join(dir_path, file_name)
                            content_bytes = base64.b64decode(attachment.get('contentBytes'))

                            if not os.path.exists(file_path):
                                with open(file_path, 'wb') as f:
                                    f.write(content_bytes)
                                attachment_list.append(file_path)

                email_attachment_list.append({'email': message, 'attachments': attachment_list})
    return email_attachment_list

def get_archive_folder_id():
    endpoint = f'https://graph.microsoft.com/v1.0/users/{CLIENT_EMAIL}/mailFolders'
    auth_provider = AuthProvider(CLIENT_ID, CLIENT_SECRET, TENANT_ID)

    response = requests.get(endpoint, auth=auth_provider)

    if response.status_code == 200:
        folders = response.json().get('value', [])
        for folder in folders:
            if folder.get('displayName') == 'Archive' or folder.get('displayName') == 'Archief':
                return folder.get('id')

    print(f"Archive folder not found for user: {CLIENT_EMAIL}")
    return None

def move_email_to_archive(action, email_id, archive_folder_id):   
    endpoint = f'https://graph.microsoft.com/v1.0/users/{CLIENT_EMAIL}/messages/{email_id}/move'
    auth_provider = AuthProvider(CLIENT_ID, CLIENT_SECRET, TENANT_ID)
    if not action.test:
        payload = {
            'destinationId': archive_folder_id,  # Replace with the ID of your archive folder
        }
        response = requests.post(endpoint, json=payload, auth=auth_provider)

        if response.status_code != 200:
            print(f"Failed to move email to archive. Status code: {response.status_code}, Error: {response.text}")