"""
core/gsheet_api.py — Google Sheets API client.

Reads contact rows from a Google Sheet using a Service Account.
"""

import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

import config

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


def _get_client() -> gspread.Client:
    """Authenticate and return an authorised gspread client."""
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        config.GOOGLE_CREDENTIALS_FILE, SCOPES
    )
    return gspread.authorize(creds)


def read_contacts(sheet_url: str) -> pd.DataFrame:
    """Read all rows from the first worksheet of *sheet_url*.

    Returns:
        A DataFrame where each row represents one contact.
        Column names are taken from the header row of the sheet.
    """
    client = _get_client()
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.sheet1
    records = worksheet.get_all_records()
    return pd.DataFrame(records)


def get_worksheet(sheet_url: str) -> gspread.Worksheet:
    """Return the first worksheet of the specified spreadsheet."""
    client = _get_client()
    spreadsheet = client.open_by_url(sheet_url)
    return spreadsheet.sheet1


def get_spreadsheet_info(sheet_url: str) -> dict[str, str]:
    """Retrieve spreadsheet title and ID given its URL.

    Args:
        sheet_url: Public or shared Google Sheet URL.

    Returns:
        dict with 'title' and 'id'.
    """
    client = _get_client()
    spreadsheet = client.open_by_url(sheet_url)
    return {
        "title": spreadsheet.title,
        "id": spreadsheet.id,
    }


def read_contact_rows(worksheet: gspread.Worksheet) -> tuple[list[str], list[dict]]:
    """Read all contact rows along with header and 1-indexed sheet row numbers.

    Returns:
        A tuple of (headers, records), where each record contains:
        - '_row_number': int (1-indexed row number in the worksheet)
        - key-value pairs corresponding to column headers
    """
    headers = [str(h).strip() for h in worksheet.row_values(1)]
    raw_records = worksheet.get_all_records()

    records = []
    # Data rows start at row 2 (row 1 is header)
    for idx, row in enumerate(raw_records, start=2):
        row_dict = dict(row)
        row_dict["_row_number"] = idx
        records.append(row_dict)

    return headers, records


def batch_update_cells(
    worksheet: gspread.Worksheet,
    data: list[dict],
) -> None:
    """Batch update multiple cell ranges in the worksheet.

    Args:
        worksheet: The gspread Worksheet object.
        data: List of dicts formatted for worksheet.batch_update:
                [{"range": "F2", "values": [["SUCCESS"]]}, ...]
    """
    if not data:
        return
    worksheet.batch_update(data)
