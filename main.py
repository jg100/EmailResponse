# Importing os and pickle module in program
import base64
import os
import pickle
# Creating utils for Gmail APIs  
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup
# Importing libraries for encoding/decoding messages in base64  
from base64 import urlsafe_b64decode, urlsafe_b64encode
# Importing libraries for dealing with the attachment of MIME types in Gmail  
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from mimetypes import guess_type as guess_mime_type

# Request all access from Gmail APIs and project  
SCOPES = ['https://mail.google.com/']
OurEmailID = 'OurMail@gmail.com'  # giving our Gmail Id


# using a default function to authenticate Gmail APIs
def authenticateGmailAPIs():
    creds = None
    # Authorizing the Gmail APIs with tokens of pickles  
    if os.path.exists("token.pickle"):  # using if else statement
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
            # If there are no valid credentials available in device, we will let the user sign in manually
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cred2.json',
                SCOPES)  # downloaded credential name
            creds = flow.run_local_server(port=0)  # running credentials
        # Save the credentials for the next run  
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('Gmail', 'v1', credentials=creds)  # using Gmail to authenticate


def searchMail(keyword, service):
    result = service.users().messages().list(userId='me').execute()

    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
    del messages[50:]
    print(messages)

    for msg in messages:
        try:
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            print("Start try...")
            # Use try-except to avoid any Errors

            # Get value of 'payload' from dictionary 'txt'
            payload = txt['payload']
            headers = payload['headers']

            # Look for Subject and Sender Email in the headers
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']

            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-", "+").replace("_", "/")
            decoded_data = base64.b64decode(data)

            # Now, the data obtained is in lxml. So, we will parse
            # it with BeautifulSoup library
            soup = BeautifulSoup(decoded_data, "lxml")
            body = soup.body()

            if sender == "noreply@123formbuilder.com":
                print("** Email data **")
                 # Printing the subject, sender's email and message
                print("Subject: ", subject)
                print("From: ", sender)
                print("Message: ", body)
                print('\n')
        except:
            print("Exception...")
            pass


# Get the Gmail API service by calling the function
service = authenticateGmailAPIs()
searchMail("n/a", service)
