""""""
import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

GMAIL_SCOPES = os.environ.get("GMAIL_SCOPES")

SALESFORCE_USERNAME = os.environ.get("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = os.environ.get("SALESFORCE_PASSWORD")
SALESFORCE_SECURITY_TOKEN = os.environ.get("SALESFORCE_SECURITY_TOKEN")

