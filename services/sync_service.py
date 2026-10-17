"""
services/sync_service.py — Business logic for syncing contacts to HubSpot.

Orchestrates reading from Google Sheets and upserting into HubSpot.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from requests.models import HTTPError

import config
from core import gsheet_api, hubspot_api


class FindContact:
    """Fetch and index HubSpot contacts for a list of records.

    Lookup strategy (per record):
        1. If the record has a non-empty ``email`` field, look up by email.
        2. If the record has no email but has a non-empty ``phone`` field,
            fall back to phone lookup.
        3. Records that have neither field are silently skipped.

    Contacts are retrieved from HubSpot via pagination using
    ``hubspot_api.retrieve_contacts`` and indexed in-memory for quick lookup.

    Usage::

        finder = FindContact()
        records = [
            {"email": "alice@example.com", "phone": "0901234567"},
            {"email": "", "phone": "0987654321"},
        ]
        id_map = finder.find(records)
        # id_map -> {"alice@example.com": "12345", "0987654321": "67890"}
    """

    def __init__(self, limit: int = 10) -> None:
        self.limit = limit
        self._next_cursor: Optional[str] = None
        self._has_more: bool = True
        self._email_map: dict[str, str] = {}
        self._phone_map: dict[str, str] = {}
        self._load_next_page()

    def _load_next_page(self) -> bool:
        """Load next page of contacts from HubSpot API.

        Returns True if a page was loaded and there is another page, False otherwise.
        """
        if not self._has_more:
            return False

        contacts, next_cursor = hubspot_api.retrieve_contacts(
            limit=self.limit,
            after=self._next_cursor,
            properties=["email", "phone"],
        )

        self._next_cursor = next_cursor or None
        self._has_more = bool(next_cursor)

        for contact in contacts:
            contact_id = str(contact.get("id", ""))
            props = contact.get("properties", {}) or {}
            email = str(props.get("email", "") or "").strip().lower()
            phone = str(props.get("phone", "") or "").strip()

            if email and email not in self._email_map:
                self._email_map[email] = contact_id
            if phone and phone not in self._phone_map:
                self._phone_map[phone] = contact_id

        return self._has_more

    def find(self, records: list[dict]) -> dict[str, str]:
        """Look up HubSpot contact IDs for a collection of records.

        Each record is a dict that may contain `"email"` and/or
        `"phone"` keys. The method applies an email-first strategy:

        * Records **with** a valid email are looked up by email.
        * Records **without** a valid email but **with** a valid phone are
            looked up by phone number.
        * Records with neither are ignored.

        Args:
            records: A list of dicts, each representing one row of contact
                data (e.g. a row read from Google Sheets).

        Returns:
            A flat `dict` mapping each identifier (email or phone) to the
            corresponding HubSpot contact ID. Identifiers not found in
            HubSpot are absent from the result.
        """
        if not records:
            return {}

        id_map: dict[str, str] = {}

        for record in records:
            raw_email = str(record.get("email", "") or "").strip()
            raw_phone = str(record.get("phone", "") or "").strip()

            if raw_email:
                normalized_email = raw_email.lower()
                contact_id = self._find_by_email(normalized_email)
                if contact_id:
                    id_map[raw_email] = contact_id
            elif raw_phone:
                contact_id = self._find_by_phone(raw_phone)
                if contact_id:
                    id_map[raw_phone] = contact_id

        return id_map

    def _find_by_email(self, raw_email: str) -> str:
        """Find contact by email from cached contacts `_email_map`.
        If email not found, load next page of contacts and try again.
        If email is not found after loading all pages, return "".

        Args:
            raw_email: Email to look up.

        Returns:
            HubSpot contact ID if found, empty string otherwise.
        """
        normalized_email = raw_email.lower()
        if normalized_email in self._email_map:
            return self._email_map[normalized_email]
        while self._has_more:
            self._load_next_page()
            if normalized_email in self._email_map:
                return self._email_map[normalized_email]
        return ""

    def _find_by_phone(self, raw_phone: str) -> str:
        """Find contact by phone from cached contacts `_phone_map`.
        If phone not found, load next page of contacts and try again.
        If phone is not found after loading all pages, return "".

        Args:
            raw_phone: Phone number to look up.

        Returns:
            HubSpot contact ID if found, empty string otherwise.
        """
        if raw_phone in self._phone_map:
            return self._phone_map[raw_phone]
        while self._has_more:
            self._load_next_page()
            if raw_phone in self._phone_map:
                return self._phone_map[raw_phone]
        return ""


@dataclass
class SyncResult:
    """Summary of a completed sync run."""

    created: int = 0
    updated: int = 0
    failed: int = 0
    errors: List[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        """Total rows processed."""
        return self.created + self.updated + self.failed


def _row_to_properties(record: dict) -> dict:
    """Convert a sheet row dictionary to a HubSpot properties dict.

    Drops internal metadata fields like '_row_number', 'status', 'hubspot_id'
    and empty/None values.
    """
    excluded_fields = {"_row_number", "status", "hubspot_id"}
    return {
        key: str(value).strip()
        for key, value in record.items()
        if key not in excluded_fields and value is not None and str(value).strip() != ""
    }


def _validate_contact_data(record: dict) -> tuple[bool, str]:
    """Validate contact data before syncing.

    Currently temporary pass: considers data valid if either email or phone is present.
    Returns (is_valid, error_message).
    """
    email = str(record.get("email", "") or "").strip()
    phone = str(record.get("phone", "") or "").strip()

    if not email and not phone:
        return False, "Thiếu cả email và phone"
    return True, ""


def _col_idx_to_letter(col_idx: int) -> str:
    """Convert 1-indexed column number to
    Excel column letter (e.g. 1 -> 'A', 27 -> 'AA').
    """
    result = []
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        result.append(chr(65 + remainder))
    return "".join(reversed(result))


def run_sync() -> SyncResult:
    """Read contacts from Google Sheets and upsert them into HubSpot.

    Only processes rows with status="NEW".
    Updates status ('SUCCESS', 'UPDATED', 'ERROR') and HubSpot ID in Google Sheet
    via a batch update call.

    Returns:
        A SyncResult with counts of created, updated, and failed records.
    """
    result = SyncResult()

    worksheet = gsheet_api.get_worksheet(config.GOOGLE_SHEET_URL)
    headers, records = gsheet_api.read_contact_rows(worksheet)

    # Determine 1-indexed column indices for 'status' and 'hubspot_id'
    # Headers may have varying cases, normalize for lookup
    headers_lower = [h.lower() for h in headers]

    status_col_idx = (
        headers_lower.index("status") + 1 if "status" in headers_lower else None
    )
    hubspot_id_col_idx = (
        headers_lower.index("hubspot_id") + 1 if "hubspot_id" in headers_lower else None
    )

    # Filter rows that have status="NEW"
    new_records = [
        rec
        for rec in records
        if str(rec.get("status", "") or "").strip().upper() == "NEW"
        or str(rec.get("status", "") or "").strip().upper() == "ERROR"
    ]

    if not new_records:
        return result

    # Find matching HubSpot contacts (Email -> Phone fallback)
    finder = FindContact()
    id_map = finder.find(new_records)

    sheet_updates: list[dict] = []

    for rec in new_records:
        row_num = rec["_row_number"]
        raw_email = str(rec.get("email", "") or "").strip()
        raw_phone = str(rec.get("phone", "") or "").strip()

        # Step 1: Validate data (temporary pass check)
        is_valid, val_err = _validate_contact_data(rec)
        if not is_valid:
            result.failed += 1
            result.errors.append(f"Row {row_num}: {val_err}")
            if status_col_idx:
                sheet_updates.append(
                    {
                        "range": f"{_col_idx_to_letter(status_col_idx)}{row_num}",
                        "values": [["ERROR"]],
                    }
                )
            continue

        # Step 2: Determine if contact exists in HubSpot
        existing_id = ""
        if raw_email:
            existing_id = id_map.get(raw_email, "")
        elif raw_phone:
            existing_id = id_map.get(raw_phone, "")

        properties = _row_to_properties(rec)

        # Step 3: Create or Update HubSpot Contact
        try:
            if existing_id:
                hubspot_api.update_contact(existing_id, properties)
                hubspot_id = existing_id
                status = "UPDATED"
                result.updated += 1
            else:
                resp = hubspot_api.create_contact(properties)
                hubspot_id = str(resp.get("id", ""))
                status = "SUCCESS"
                result.created += 1

            if status_col_idx:
                sheet_updates.append(
                    {
                        "range": f"{_col_idx_to_letter(status_col_idx)}{row_num}",
                        "values": [[status]],
                    }
                )
            if hubspot_id_col_idx and hubspot_id:
                sheet_updates.append(
                    {
                        "range": f"{_col_idx_to_letter(hubspot_id_col_idx)}{row_num}",
                        "values": [[hubspot_id]],
                    }
                )
        except HTTPError as http_error:
            result.failed += 1
            response = http_error.response
            result.errors.append(
                f"Row {row_num}: {response.status_code}"
                + f" - {response.json().get('category')}"
                + f"\nJSON: {response.json()}"
            )
            if status_col_idx:
                sheet_updates.append(
                    {
                        "range": f"{_col_idx_to_letter(status_col_idx)}{row_num}",
                        "values": [["ERROR"]],
                    }
                )
        except Exception as exc:  # noqa: BLE001
            result.failed += 1
            identifier = raw_email or raw_phone or f"Row {row_num}"
            result.errors.append(f"{identifier}: {exc}")
            if status_col_idx:
                sheet_updates.append(
                    {
                        "range": f"{_col_idx_to_letter(status_col_idx)}{row_num}",
                        "values": [["ERROR"]],
                    }
                )

    # Step 4: Batch update back to Google Sheets
    if sheet_updates:
        gsheet_api.batch_update_cells(worksheet, sheet_updates)

    return result
