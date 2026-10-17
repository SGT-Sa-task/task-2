"""
services/sheet_storage_service.py — Manage local Google Sheets records and bot info.

Handles reading bot service account email from storage/bot-account.txt and
persisting saved spreadsheet links to storage/local-data.csv.
"""

import csv
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
BOT_ACCOUNT_FILE = STORAGE_DIR / "bot-account.txt"
LOCAL_DATA_FILE = STORAGE_DIR / "local-data.csv"

CSV_HEADERS = ["Tên của sheet", "Link", "ID Sheet", "Truy cập lần cuối"]


def extract_sheet_id_from_url(sheet_url: str) -> str:
    """Extract Google Spreadsheet ID from a standard Google Sheets URL.

    Args:
        sheet_url: Google Sheets URL string.

    Returns:
        Spreadsheet ID if matched, otherwise empty string.
    """
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_url)
    if match:
        return match.group(1)
    return ""


def get_bot_account_email(filepath: Optional[Path] = None) -> str:
    """Read the bot service account email from storage file.

    Args:
        filepath: Optional custom Path to bot-account.txt.

    Returns:
        Bot email string, or empty string if file does not exist or is empty.
    """
    path = filepath or BOT_ACCOUNT_FILE
    if not path.exists():
        return ""
    try:
        content = path.read_text(encoding="utf-8").strip()
        return content.splitlines()[0].strip() if content else ""
    except Exception:
        return ""


def load_saved_sheets(filepath: Optional[Path] = None) -> list[dict[str, str]]:
    """Load saved Google Sheet records from CSV.

    Ensures the presence of standard columns including 'ID Sheet'.

    Args:
        filepath: Optional custom Path to local-data.csv.

    Returns:
        List of dicts representing each saved sheet record.
    """
    path = filepath or LOCAL_DATA_FILE
    if not path.exists():
        return []

    records: list[dict[str, str]] = []
    try:
        with open(path, mode="r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            _ = [fn.strip() for fn in (reader.fieldnames or [])]
            for row in reader:
                clean_row = {
                    k.strip(): (v.strip() if v else "") for k, v in row.items() if k
                }
                name = clean_row.get("Tên của sheet", "")
                link = clean_row.get("Link", "")
                sheet_id = clean_row.get("ID Sheet", "") or extract_sheet_id_from_url(
                    link
                )
                last_access = clean_row.get("Truy cập lần cuối", "")

                if not name and not link:
                    continue

                records.append(
                    {
                        "Tên của sheet": name,
                        "Link": link,
                        "ID Sheet": sheet_id,
                        "Truy cập lần cuối": last_access,
                    }
                )
    except Exception:
        return []

    return records


def save_sheet_record(
    name: str,
    link: str,
    sheet_id: str = "",
    filepath: Optional[Path] = None,
) -> bool:
    """Save or update a Google Sheet record in the CSV file.

    If a sheet with the same link or sheet_id already exists, updates its title.
    Otherwise appends a new row.

    Args:
        name: Name / title of the Google Sheet.
        link: URL to the Google Sheet.
        sheet_id: Google Spreadsheet ID. If empty, extracts from URL.
        filepath: Optional custom Path to local-data.csv.

    Returns:
        True if successfully written, False otherwise.
    """
    path = filepath or LOCAL_DATA_FILE
    resolved_id = sheet_id or extract_sheet_id_from_url(link)

    existing_records = load_saved_sheets(path)

    found = False
    for rec in existing_records:
        if (resolved_id and rec.get("ID Sheet") == resolved_id) or (
            rec.get("Link") == link
        ):
            rec["Tên của sheet"] = name
            rec["Link"] = link
            rec["ID Sheet"] = resolved_id
            found = True
            break

    if not found:
        existing_records.append(
            {
                "Tên của sheet": name,
                "Link": link,
                "ID Sheet": resolved_id,
                "Truy cập lần cuối": "",
            }
        )

    return _write_records_to_csv(existing_records, path)


def update_last_accessed(
    sheet_identifier: str,
    filepath: Optional[Path] = None,
    timestamp: Optional[datetime] = None,
) -> bool:
    """Update the 'Truy cập lần cuối' column for a sheet record.

    Format required: [HH:mm] - [DD/MM/yyyy]

    Args:
        sheet_identifier: Link or Sheet ID of the target spreadsheet.
        filepath: Optional custom Path to local-data.csv.
        timestamp: Optional datetime object for formatting. Defaults to now.

    Returns:
        True if updated and saved successfully, False otherwise.
    """
    path = filepath or LOCAL_DATA_FILE
    existing_records = load_saved_sheets(path)
    now = timestamp or datetime.now()
    formatted_time = now.strftime("[%H:%M] - [%d/%m/%Y]")

    matched = False
    for rec in existing_records:
        if (
            rec.get("Link") == sheet_identifier
            or rec.get("ID Sheet") == sheet_identifier
        ):
            rec["Truy cập lần cuối"] = formatted_time
            matched = True
            break

    if matched:
        return _write_records_to_csv(existing_records, path)

    return False


def _write_records_to_csv(records: list[dict[str, str]], path: Path) -> bool:
    """Write standard records list to CSV file.

    Args:
        records: List of record dictionaries.
        path: Path to target CSV file.

    Returns:
        True if written successfully, False otherwise.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for r in records:
                writer.writerow(
                    {
                        "Tên của sheet": r.get("Tên của sheet", ""),
                        "Link": r.get("Link", ""),
                        "ID Sheet": r.get("ID Sheet", ""),
                        "Truy cập lần cuối": r.get("Truy cập lần cuối", ""),
                    }
                )
        return True
    except Exception:
        return False
