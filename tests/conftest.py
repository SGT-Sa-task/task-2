"""
tests/conftest.py — Shared pytest fixtures for the HubSpot Sync app.

Fixtures defined here are automatically available to all test modules
without explicit imports, per pytest's conftest discovery mechanism.

Key responsibilities:
- Patch environment variables so `config.py` can be imported safely
    during tests without a real .env file or live credentials.
- Provide reusable fake data (sample DataFrames, contact payloads)
    that test modules can use without re-declaring them.
"""

# import os
# from unittest.mock import patch

import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# Inject dummy env vars at MODULE LOAD TIME (before pytest collection).
#
# Why here and not in a fixture?
# config.py executes os.environ["HUBSPOT_API_KEY"] at import time.
# pytest collects (imports) test files before any fixture runs, so
# a monkeypatch fixture would be too late — the KeyError fires during
# collection. Patching os.environ here ensures the values exist the
# moment Python first imports config.
# ---------------------------------------------------------------------------
# _ENV_PATCH = patch.dict(
#     os.environ,
#     {
#         "HUBSPOT_API_KEY": "test-hubspot-api-key",
#         "GOOGLE_SHEET_URL": "https://docs.google.com/spreadsheets/d/FAKE_ID/edit",
#         "GOOGLE_CREDENTIALS_FILE": "fake_credentials.json",
#     },
# )
# _ENV_PATCH.start()

# ---------------------------------------------------------------------------
# Environment / config fixtures
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Sample data fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_contacts_df():
    """Return a small DataFrame that mimics a Google Sheets export.

    Columns mirror typical HubSpot property names so the data can be
    passed directly to ``sync_service._row_to_properties``.

    Returns:
        pd.DataFrame: Three rows — two valid contacts and one with a
        missing email to exercise the skip-on-missing-email path.
    """
    return pd.DataFrame(
        [
            {
                "email": "alice@example.com",
                "firstname": "Alice",
                "lastname": "Smith",
                "phone": "0901234567",
            },
            {
                "email": "bob@example.com",
                "firstname": "Bob",
                "lastname": "Jones",
                "phone": "",
            },
            {
                "email": "",  # intentionally blank — should be skipped
                "firstname": "NoEmail",
                "lastname": "Person",
                "phone": "0909999999",
            },
        ]
    )


@pytest.fixture()
def valid_contact_properties():
    """Return a minimal HubSpot properties dict for a single contact.

    Returns:
        dict: Property names and string values suitable for
        ``hubspot_api.create_contact`` / ``hubspot_api.update_contact``.
    """
    return {
        "email": "alice@example.com",
        "firstname": "Alice",
        "lastname": "Smith",
    }
