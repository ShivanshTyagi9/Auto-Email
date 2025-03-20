import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SERVICE_ACCOUNT_FILE = "credentials.json"