""""""
import base64
import os
from collections import defaultdict

from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from settings import GMAIL_SCOPES
from src.sentiment import get_sentiment


class GoogleApi:
    def __init__(self, service_name: str, scopes: [str]):
        self.service_name = service_name
        self.scopes = scopes
        self.service = None

    def auth(self):
        creds = Credentials.from_authorized_user_file('token.json', self.scopes) if os.path.exists('token.json') else None
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        try:
            self.service = build(self.service_name, 'v1', credentials=creds)
        except HttpError as err:
            print(err)


class GMail:
    def __init__(self):
        self.gmail = GoogleApi('gmail', GMAIL_SCOPES.split(','))
        self.gmail.auth()

    def scan_messages(self, n: int = 10, email_only: bool = True) -> dict:
        messages = self.gmail.service.users().messages().list(userId='me', maxResults=n).execute()
        # next_page_token, result_size_estimate = messages['nextPageToken'], messages['resultSizeEstimate']

        plain_text_messages = defaultdict(list)

        def recurse(msg):
            for part in msg:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                elif part['mimeType'] == 'text/html':
                    return BeautifulSoup(base64.urlsafe_b64decode(part['body']['data'].decode('utf-8'))).text
                elif 'parts' in part:
                    return recurse(part['parts'])
                else:
                    raise Exception('Does this case exist?')

        for email in messages['messages']:
            msg = self.gmail.service.users().messages().get(userId='me', id=email['id']).execute()

            sender = [header for header in msg['payload']['headers'] if header['name'] == 'From'][0]['value']
            if email_only:
                try:
                    sender = sender.split('<')[1].split('>')[0]
                except:
                    raise Exception("Can't parse sender email")

            if msg['payload']['mimeType'] == 'text/plain':
                plain_text_messages[sender].append(base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8'))
            elif msg['payload']['mimeType'] == 'text/html':
                plain_text_messages[sender].append(BeautifulSoup(base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')).text)
            elif msg['payload']['mimeType'].startswith('multipart'):
                plain_text_messages[sender].append(recurse(msg['payload']['parts']))
            else:
                print(msg['payload']['mimeType'])
                raise Exception('Unknown email type')

        def mean(numbers): return sum(numbers) / len(numbers)
        return {key: mean([get_sentiment(v) for v in val]) for key, val in plain_text_messages.items()}


