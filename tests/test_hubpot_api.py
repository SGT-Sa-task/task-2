from requests import HTTPError

from core import hubspot_api


def test_retrieve_contacts():
    contacts, after = hubspot_api.retrieve_contacts(
        limit=5, properties=["email", "phone"]
    )
    print("#" * 10, after, sep="\n")
    print(bool(after))


def test_delete_contact(mocker):
    """delete_contact() should call DELETE on HubSpot API endpoint."""
    mock_delete = mocker.patch("core.hubspot_api.requests.delete")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 204
    mock_delete.return_value = mock_response

    res = hubspot_api.delete_contact("12345")
    assert res is True
    mock_delete.assert_called_once()


def test_get_formatted_contacts(mocker):
    """get_formatted_contacts() should format fields and concatenate names."""
    mock_retrieve = mocker.patch("core.hubspot_api.retrieve_contacts")
    mock_raw = [
        {
            "id": "1001",
            "properties": {
                "firstname": "Nguyen",
                "lastname": "Van A",
                "email": "a@example.com",
                "phone": "+84901234567",
            },
        },
        {
            "id": "1002",
            "properties": {
                "firstname": "Alice",
                "lastname": "",
                "email": "alice@example.com",
                "phone": "",
            },
        },
        {
            "id": "1003",
            "properties": {
                "firstname": "",
                "lastname": "",
                "email": "",
                "phone": "",
            },
        },
    ]
    mock_retrieve.return_value = (mock_raw, "cursor_abc123")

    contacts, next_cursor = hubspot_api.get_formatted_contacts(limit=5, after="   ")
    assert next_cursor == "cursor_abc123"
    assert len(contacts) == 3
    assert contacts[0] == {
        "id": "1001",
        "name": "Nguyen Van A",
        "email": "a@example.com",
        "phone": "+84901234567",
    }
    assert contacts[1] == {
        "id": "1002",
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "—",
    }
    assert contacts[2] == {
        "id": "1003",
        "name": "—",
        "email": "—",
        "phone": "—",
    }
    mock_retrieve.assert_called_once_with(
        limit=5,
        after=None,
        properties=["firstname", "lastname", "email", "phone"],
    )


class TestRealHubSpotAPI:
    def test_create_contact(self):
        """Test create contact"""
        properties: dict = {
            "email": "test007@example.com",
            "phone": "+84360000003",
            "firstname": "Test",
            "lastname": "User001",
        }
        try:
            result = hubspot_api.create_contact(properties)
            print(f"===> Result after create contact: {result}")
            assert True
        except HTTPError as e:
            print(f"===> Error when create contact: {e.response.json()}")
            print(f"===> STATUS CODE: {e.response.status_code}")
            assert False
