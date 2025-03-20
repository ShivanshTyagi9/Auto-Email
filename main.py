import time
from email_fetcher import get_latest_unread_emails, mark_email_as_read
from email_responder import generate_email_reply
from email_sender import send_email

def auto_reply():
    while True:
        print("Checking for new emails...")
        unread_emails = get_latest_unread_emails()
        if unread_emails:
            print(f"📩 Found {len(unread_emails)} unread emails!")

            for email_data in unread_emails:
                print(f"New email from {email_data['sender']} - {email_data['subject']}")
                reply_text = generate_email_reply(email_data)
                send_email(reply_text, email_data["sender"], email_data["subject"])
                print(f"Replied to {email_data['sender']}!")

                mark_email_as_read(email_data["id"])
                print("Marked email as read.")
        else:
            print("No new emails found.")

        print("Waiting for 30seconds...")
        time.sleep(30)

if __name__ == "__main__":
    auto_reply()
