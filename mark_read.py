from googleapiclient.discovery import build
from email_fetcher import get_gmail_service

def mark_all_emails_as_read():
    service = get_gmail_service()
    
    # Get all unread emails
    results = service.users().messages().list(userId="me", labelIds=["UNREAD"]).execute()
    messages = results.get("messages", [])

    if not messages:
        print("✅ No unread emails found!")
        return

    print(f"🔹 Marking {len(messages)} emails as read...")

    for message in messages:
        msg_id = message["id"]
        service.users().messages().modify(userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}).execute()
    
    print("✅ All unread emails have been marked as read!")

if __name__ == "__main__":
    mark_all_emails_as_read()
