"""
tests/test_gsheet_api.py — Unit tests for core/gsheet_api.py.

All external calls (Google credentials, gspread) are mocked so tests
run without a real credentials file or internet connection.
"""

import os

import gspread
import pandas as pd
import pytest
from pytest_mock import MockerFixture

from core import gsheet_api


class TestGetClient:
    """Tests for the private helper ``gsheet_api._get_client``."""

    def test_returns_authorised_client(self, mocker: MockerFixture):
        """_get_client() should return whatever gspread.authorize returns.

        We mock both external calls:
        - ServiceAccountCredentials.from_json_keyfile_name
        - gspread.authorize

        Then we assert that _get_client() chains them correctly and
        returns the client object.
        """
        # --- Arrange ---------------------------------------------------------
        # Tạo object giả đại diện cho "credentials" và "gspread client"
        fake_creds = mocker.MagicMock(name="fake_creds")
        fake_client = mocker.MagicMock(name="fake_client")

        # Thay thế hàm thật bằng hàm giả:
        # Khi code gọi ServiceAccountCredentials.from_json_keyfile_name(...)
        # → trả về fake_creds thay vì đọc file thật
        mock_from_keyfile = mocker.patch(
            "core.gsheet_api.ServiceAccountCredentials.from_json_keyfile_name",
            return_value=fake_creds,
        )

        # Khi code gọi gspread.authorize(...)
        # → trả về fake_client thay vì kết nối Google thật
        mock_authorize = mocker.patch(
            "core.gsheet_api.gspread.authorize",
            return_value=fake_client,
        )

        # --- Act -------------------------------------------------------------
        result = gsheet_api._get_client()

        # --- Assert ----------------------------------------------------------
        # 1. Kiểm tra from_json_keyfile_name được gọi đúng tham số
        mock_from_keyfile.assert_called_once_with(
            gsheet_api.config.GOOGLE_CREDENTIALS_FILE,
            gsheet_api.SCOPES,
        )

        # 2. Kiểm tra gspread.authorize nhận credentials từ bước trên
        mock_authorize.assert_called_once_with(fake_creds)

        # 3. Kiểm tra hàm trả về đúng client object
        assert result is fake_client

    def test_uses_credentials_file_from_config(self, mocker: MockerFixture):
        """_get_client() must read the credentials path from config,
        not from a hardcoded string.

        This guards against accidentally hardcoding 'credentials.json'
        directly in the function body instead of using config.
        """
        # --- Arrange ---------------------------------------------------------
        mock_from_keyfile = mocker.patch(
            "core.gsheet_api.ServiceAccountCredentials.from_json_keyfile_name"
        )
        mock_authorize = mocker.patch("core.gsheet_api.gspread.authorize")

        # Ghi đè config.GOOGLE_CREDENTIALS_FILE thành giá trị khác
        mocker.patch(
            "core.gsheet_api.config.GOOGLE_CREDENTIALS_FILE",
            "custom/path/creds.json",
        )

        # --- Act -------------------------------------------------------------
        gsheet_api._get_client()

        # --- Assert ----------------------------------------------------------
        mock_authorize.assert_called_once()
        # Nếu code dùng config đúng, tham số phải là "custom/path/creds.json"
        mock_from_keyfile.assert_called_once_with(
            "custom/path/creds.json",
            gsheet_api.SCOPES,
        )


class TestReadContacts:
    """Tests for ``gsheet_api.read_contacts``."""

    def test_reads_records_and_returns_dataframe(self, mocker: MockerFixture):
        """read_contacts() should open the spreadsheet by URL, get records

        from sheet1, and return them formatted as a pandas DataFrame.
        """
        # --- Arrange ---
        fake_url = "https://docs.google.com/spreadsheets/d/test-sheet-id"
        fake_records = [
            {"email": "alice@example.com", "firstname": "Alice"},
            {"email": "bob@example.com", "firstname": "Bob"},
        ]

        # Giả lập worksheet.get_all_records()
        mock_worksheet = mocker.MagicMock()
        mock_worksheet.get_all_records.return_value = fake_records

        # Giả lập spreadsheet.sheet1
        mock_spreadsheet = mocker.MagicMock()
        mock_spreadsheet.sheet1 = mock_worksheet

        # Giả lập client.open_by_url()
        mock_client = mocker.MagicMock()
        mock_client.open_by_url.return_value = mock_spreadsheet

        # Giả lập _get_client() trả về mock_client
        mock_get_client = mocker.patch(
            "core.gsheet_api._get_client", return_value=mock_client
        )

        # --- Act ---
        df = gsheet_api.read_contacts(fake_url)

        # --- Assert ---
        mock_get_client.assert_called_once()
        mock_client.open_by_url.assert_called_once_with(fake_url)
        mock_worksheet.get_all_records.assert_called_once()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df["email"]) == ["alice@example.com", "bob@example.com"]

    def test_returns_empty_dataframe_when_sheet_is_empty(self, mocker: MockerFixture):
        """read_contacts() should return an empty DataFrame when sheet has

        no records.
        """
        mock_worksheet = mocker.MagicMock()
        mock_worksheet.get_all_records.return_value = []

        mock_spreadsheet = mocker.MagicMock()
        mock_spreadsheet.sheet1 = mock_worksheet

        mock_client = mocker.MagicMock()
        mock_client.open_by_url.return_value = mock_spreadsheet

        mocker.patch("core.gsheet_api._get_client", return_value=mock_client)

        df = gsheet_api.read_contacts("https://docs.google.com/sheet")

        assert isinstance(df, pd.DataFrame)
        assert df.empty


class TestGetSpreadsheetInfo:
    """Tests for ``gsheet_api.get_spreadsheet_info``."""

    def test_get_spreadsheet_info_success(self, mocker: MockerFixture):
        """get_spreadsheet_info() should return dict with title and id."""
        fake_url = "https://docs.google.com/spreadsheets/d/test-sheet-id"
        mock_spreadsheet = mocker.MagicMock()
        mock_spreadsheet.title = "Sample Sheet Title"
        mock_spreadsheet.id = "test-sheet-id"

        mock_client = mocker.MagicMock()
        mock_client.open_by_url.return_value = mock_spreadsheet

        mocker.patch("core.gsheet_api._get_client", return_value=mock_client)

        info = gsheet_api.get_spreadsheet_info(fake_url)

        assert info == {
            "title": "Sample Sheet Title",
            "id": "test-sheet-id",
        }
        mock_client.open_by_url.assert_called_once_with(fake_url)


class TestRealGSheetAPI:
    """Integration test suite connecting to Google Sheets API with real credentials."""

    @pytest.mark.skipif(
        not os.path.exists("credentials.json"),
        reason="Requires real credentials.json file to run integration test",
    )
    def test_get_client(self):
        """Authenticate with the actual credentials.json file.

        Verifies that _get_client returns an active, authorized gspread.Client
        without raising any authentication exceptions.
        """
        client = gsheet_api._get_client()

        assert isinstance(client, gspread.Client)
        assert client.http_client is not None

    @pytest.mark.skipif(
        not os.path.exists("credentials.json") or not os.getenv("GOOGLE_SHEET_URL"),
        reason="Requires credentials.json and GOOGLE_SHEET_URL to run",
    )
    def test_read_contacts_real(self):
        """Read contacts from the real Google Sheet configured in .env."""
        import config

        df = gsheet_api.read_contacts(config.GOOGLE_SHEET_URL)
        row_count = len(df)

        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert row_count == 5
        print("\n", "#" * 50, "\n", df.head())
