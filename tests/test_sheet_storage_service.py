"""
tests/test_sheet_storage_service.py — Unit tests for services/sheet_storage_service.py.
"""

from datetime import datetime
from pathlib import Path

from services import sheet_storage_service


def test_extract_sheet_id_from_url():
    """Verify spreadsheet ID extraction from various URL formats."""
    url = (
        "https://docs.google.com/spreadsheets/d/"
        "1bEQbukGVRx4IekbOMc1dafK09_k3TisrsANpKzuCPls/edit?gid=0#gid=0"
    )
    sheet_id = sheet_storage_service.extract_sheet_id_from_url(url)
    assert sheet_id == "1bEQbukGVRx4IekbOMc1dafK09_k3TisrsANpKzuCPls"

    invalid_url = "https://example.com/not-a-google-sheet"
    assert sheet_storage_service.extract_sheet_id_from_url(invalid_url) == ""


def test_get_bot_account_email(tmp_path: Path):
    """Test reading bot account email from file."""
    fake_file = tmp_path / "bot-account.txt"
    fake_file.write_text(
        "bot-service@project.iam.gserviceaccount.com\n", encoding="utf-8"
    )

    email = sheet_storage_service.get_bot_account_email(filepath=fake_file)
    assert email == "bot-service@project.iam.gserviceaccount.com"

    non_existent = tmp_path / "missing.txt"
    assert sheet_storage_service.get_bot_account_email(filepath=non_existent) == ""


def test_load_and_save_sheet_record(tmp_path: Path):
    """Test saving a new sheet record and retrieving it."""
    csv_file = tmp_path / "local-data.csv"

    # Initially empty
    assert sheet_storage_service.load_saved_sheets(csv_file) == []

    # Save first sheet
    saved = sheet_storage_service.save_sheet_record(
        name="Sales 2026",
        link="https://docs.google.com/spreadsheets/d/abc12345/edit",
        sheet_id="abc12345",
        filepath=csv_file,
    )
    assert saved is True

    records = sheet_storage_service.load_saved_sheets(csv_file)
    assert len(records) == 1
    assert records[0]["Tên của sheet"] == "Sales 2026"
    assert records[0]["ID Sheet"] == "abc12345"
    assert records[0]["Link"] == "https://docs.google.com/spreadsheets/d/abc12345/edit"
    assert records[0]["Truy cập lần cuối"] == ""

    # Update existing sheet name with same link
    sheet_storage_service.save_sheet_record(
        name="Sales 2026 Renamed",
        link="https://docs.google.com/spreadsheets/d/abc12345/edit",
        sheet_id="abc12345",
        filepath=csv_file,
    )
    records_after = sheet_storage_service.load_saved_sheets(csv_file)
    assert len(records_after) == 1
    assert records_after[0]["Tên của sheet"] == "Sales 2026 Renamed"


def test_update_last_accessed(tmp_path: Path):
    """Test updating the last accessed timestamp in [HH:mm] - [DD/MM/yyyy] format."""
    csv_file = tmp_path / "local-data.csv"
    link = "https://docs.google.com/spreadsheets/d/xyz987/edit"

    sheet_storage_service.save_sheet_record(
        name="Customer Data",
        link=link,
        sheet_id="xyz987",
        filepath=csv_file,
    )

    fixed_time = datetime(2026, 10, 17, 9, 45)
    updated = sheet_storage_service.update_last_accessed(
        sheet_identifier=link,
        filepath=csv_file,
        timestamp=fixed_time,
    )
    assert updated is True

    records = sheet_storage_service.load_saved_sheets(csv_file)
    assert len(records) == 1
    assert records[0]["Truy cập lần cuối"] == "[09:45] - [17/10/2026]"
