from requests import HTTPError

from core import hubspot_api


def test_retrieve_contacts():
    contacts, after = hubspot_api.retrieve_contacts(
        limit=5, properties=["email", "phone"]
    )
    print("#" * 10, after, sep="\n")
    print(bool(after))


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
