import base64
from email.mime.text import MIMEText
from email_fetcher import get_gmail_service

def send_email(reply_text, recipient, subject):
    service = get_gmail_service()
    
    message = MIMEText(reply_text)
    message["to"] = recipient
    message["subject"] = "Re: " + subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
