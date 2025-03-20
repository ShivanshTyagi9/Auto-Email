import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_gmail_service():
    creds = None

    # Load token if it exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no credentials or expired, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0, open_browser=True)

        # Save credentials for future use
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

def get_latest_unread_emails():
    service = get_gmail_service()
    results = service.users().messages().list(userId="me", labelIds=["UNREAD"]).execute()
    messages = results.get("messages", [])

    if not messages:
        return []

    unread_emails = []
    for msg in messages:
        msg_id = msg["id"]
        message = service.users().messages().get(userId="me", id=msg_id).execute()

        email_data = {
            "id": msg_id,
            "sender": next(header["value"] for header in message["payload"]["headers"] if header["name"] == "From"),
            "subject": next(header["value"] for header in message["payload"]["headers"] if header["name"] == "Subject"),
            "body": message.get("snippet", "No content available"),
        }

        unread_emails.append(email_data)

    return unread_emails

def mark_email_as_read(email_id):
    """ Marks an email as read by removing the 'UNREAD' label """
    service = get_gmail_service()
    service.users().messages().modify(userId="me", id=email_id, body={"removeLabelIds": ["UNREAD"]}).execute()
