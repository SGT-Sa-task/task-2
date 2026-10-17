"""
tests/test_sync_service.py — Unit tests for sync_service.py.
"""

from unittest.mock import call, patch

from services.sync_service import FindContact, restore_created_contacts, run_sync


def test_find_contact_empty_records():
    finder = FindContact()
    result = finder.find([])
    assert result == {}


@patch("services.sync_service.hubspot_api.retrieve_contacts")
def test_find_contact_pagination_and_lookup(mock_retrieve):
    # Simulate 2 pages from HubSpot API
    page_1_contacts = [
        {
            "id": "101",
            "properties": {"email": "alice@example.com", "phone": "0901234567"},
        },
        {
            "id": "102",
            "properties": {"email": "bob@example.com", "phone": "0912345678"},
        },
    ]
    page_2_contacts = [
        {
            "id": "103",
            "properties": {"email": "", "phone": "0987654321"},
        },
    ]

    mock_retrieve.side_effect = [
        (page_1_contacts, "cursor_token_123"),
        (page_2_contacts, ""),
    ]

    finder = FindContact()
    records = [
        {"email": "Alice@example.com", "phone": "0901234567"},  # Matches email
        {"email": "", "phone": "0987654321"},  # Matches phone
        {"email": "charlie@example.com", "phone": "0999999999"},  # Not in HubSpot
        {"email": "", "phone": ""},  # Empty row
    ]

    id_map = finder.find(records)

    assert id_map == {
        "Alice@example.com": "101",
        "0987654321": "103",
    }
    assert mock_retrieve.call_count == 2
    mock_retrieve.assert_has_calls(
        [
            call(limit=10, after=None, properties=["email", "phone"]),
            call(limit=10, after="cursor_token_123", properties=["email", "phone"]),
        ]
    )


@patch("services.sync_service.gsheet_api.batch_update_cells")
@patch("services.sync_service.hubspot_api.create_contact")
@patch("services.sync_service.hubspot_api.update_contact")
@patch("services.sync_service.FindContact")
@patch("services.sync_service.gsheet_api.read_contact_rows")
def test_run_sync_flow(
    mock_read_rows,
    mock_find_contact_cls,
    mock_update_contact,
    mock_create_contact,
    mock_batch_update,
):
    from services.sync_service import run_sync

    headers = ["email", "phone", "firstname", "status", "hubspot_id"]
    records = [
        # Row 2: status is SUCCESS, should be skipped
        {
            "_row_number": 2,
            "email": "old@example.com",
            "phone": "0111",
            "firstname": "Old",
            "status": "SUCCESS",
            "hubspot_id": "999",
        },
        # Row 3: status is NEW, contact exists (update)
        {
            "_row_number": 3,
            "email": "update@example.com",
            "phone": "0222",
            "firstname": "UpdateUser",
            "status": "NEW",
            "hubspot_id": "",
        },
        # Row 4: status is NEW, contact not found (create)
        {
            "_row_number": 4,
            "email": "new@example.com",
            "phone": "0333",
            "firstname": "NewUser",
            "status": "NEW",
            "hubspot_id": "",
        },
        # Row 5: status is NEW, invalid (missing both email and phone)
        {
            "_row_number": 5,
            "email": "",
            "phone": "",
            "firstname": "InvalidUser",
            "status": "NEW",
            "hubspot_id": "",
        },
    ]
    mock_read_rows.return_value = (headers, records)

    # Mock FindContact
    mock_finder = mock_find_contact_cls.return_value
    mock_finder.find.return_value = {
        "update@example.com": "hub_123",
    }

    # Mock create response
    mock_create_contact.return_value = {"id": "hub_456"}

    result = run_sync()

    assert result.created == 1
    assert result.updated == 1
    assert result.failed == 1

    # Verify update called with hub_123
    mock_update_contact.assert_called_once_with(
        "hub_123",
        {"email": "update@example.com", "phone": "0222", "firstname": "UpdateUser"},
    )

    # Verify create called with new@example.com
    mock_create_contact.assert_called_once_with(
        {"email": "new@example.com", "phone": "0333", "firstname": "NewUser"}
    )

    # Verify batch_update_cells called with correct
    # ranges (status=col D, hubspot_id=col E)
    mock_batch_update.assert_called_once()
    _, call_data = mock_batch_update.call_args[0]
    expected_updates = [
        {"range": "D3", "values": [["UPDATED"]]},
        {"range": "E3", "values": [["hub_123"]]},
        {"range": "D4", "values": [["SUCCESS"]]},
        {"range": "E4", "values": [["hub_456"]]},
        {"range": "D5", "values": [["ERROR"]]},
    ]
    assert call_data == expected_updates


def test_run_sync_retry_mode(mocker):
    """run_sync(sync_mode='RETRY') should only process rows with status='ERROR'."""
    mocker.patch("core.gsheet_api.get_worksheet")
    mock_read_rows = mocker.patch("core.gsheet_api.read_contact_rows")
    mock_batch_update = mocker.patch("core.gsheet_api.batch_update_cells")
    mock_find_contact_cls = mocker.patch("services.sync_service.FindContact")
    mock_create_contact = mocker.patch("core.hubspot_api.create_contact")
    mocker.patch("core.hubspot_api.update_contact")

    headers = ["firstname", "email", "phone", "status", "hubspot_id"]
    records = [
        # Row 2: NEW (should be skipped in RETRY mode)
        {
            "_row_number": 2,
            "email": "new@example.com",
            "phone": "0111",
            "firstname": "NewUser",
            "status": "NEW",
            "hubspot_id": "",
        },
        # Row 3: ERROR (should be processed in RETRY mode)
        {
            "_row_number": 3,
            "email": "error@example.com",
            "phone": "0222",
            "firstname": "ErrorUser",
            "status": "ERROR",
            "hubspot_id": "",
        },
    ]
    mock_read_rows.return_value = (headers, records)

    mock_finder = mock_find_contact_cls.return_value
    mock_finder.find.return_value = {}
    mock_create_contact.return_value = {"id": "hub_789"}

    result = run_sync(sync_mode="RETRY")

    assert result.created == 1
    assert result.updated == 0
    assert result.failed == 0
    assert result.total == 1

    mock_create_contact.assert_called_once_with(
        {"email": "error@example.com", "phone": "0222", "firstname": "ErrorUser"}
    )
    mock_batch_update.assert_called_once()
    assert result.created_contact_ids == ["hub_789"]


def test_restore_created_contacts(mocker):
    """restore_created_contacts() should call delete_contact for each contact ID."""
    mock_delete = mocker.patch("services.sync_service.hubspot_api.delete_contact")

    del_count, errors = restore_created_contacts(["hub_1", "hub_2"])

    assert del_count == 2
    assert errors == []
    assert mock_delete.call_count == 2
    mock_delete.assert_any_call("hub_1")
    mock_delete.assert_any_call("hub_2")
