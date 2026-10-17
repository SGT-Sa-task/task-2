"""
config.py — Load environment variables for the HubSpot Sync app.
"""

import os

from dotenv import load_dotenv

load_dotenv()

HUBSPOT_API_KEY: str = os.environ.get("HUBSPOT_API_KEY")
GOOGLE_SHEET_URL: str = os.environ.get("GOOGLE_SHEET_URL")
GOOGLE_CREDENTIALS_FILE: str = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
