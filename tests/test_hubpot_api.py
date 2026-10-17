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
