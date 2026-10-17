"""
core/hubspot_api.py — HubSpot Contacts API client.

Supports searching a contact by email, creating a new contact,
updating an existing contact's properties, and batch-reading
multiple contacts by a given identifier property.
"""

from typing import Optional

import requests

import config

BASE_URL = "https://api.hubapi.com/crm/objects/2026-09/contacts"

# HubSpot CRM v3 batch read endpoint (supports up to 100 records/request)
BATCH_URL = f"{BASE_URL}/batch/read"


def _headers() -> dict:
    """Return authenticated request headers."""
    return {
        "Authorization": f"Bearer {config.HUBSPOT_API_KEY}",
        "Content-Type": "application/json",
    }


def find_contact_by_email(email: str) -> Optional[str]:
    """Search for a contact by email address.

    Args:
        email: The email address to look up.

    Returns:
        The HubSpot contact ID if found, otherwise None.
    """
    payload = {
        "filterGroups": [
            {
                "filters": [
                    {
                        "propertyName": "email",
                        "operator": "EQ",
                        "value": email,
                    }
                ]
            }
        ],
        "properties": ["email"],
        "limit": 1,
    }
    response = requests.post(
        f"{BASE_URL}/search",
        json=payload,
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    return results[0]["id"] if results else None


def create_contact(properties: dict) -> dict:
    """Create a new HubSpot contact.

    Args:
        properties: A dict mapping HubSpot property names to values.

    Returns:
        The API response JSON for the newly created contact.
    """
    response = requests.post(
        BASE_URL,
        json={"properties": properties, "associations": []},
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def update_contact(contact_id: str, properties: dict) -> dict:
    """Update an existing HubSpot contact.

    Args:
        contact_id: The HubSpot internal ID of the contact.
        properties: A dict of properties to update.

    Returns:
        The API response JSON for the updated contact.
    """
    response = requests.patch(
        f"{BASE_URL}/{contact_id}",
        json={"properties": properties, "associations": []},
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def batch_read_contacts(
    identifiers: list[str],
    id_property: str,
) -> list[dict]:
    """Fetch multiple contacts from HubSpot in a single batch request.

    HubSpot limits each request to 100 records. The caller is responsible
    for chunking if the list exceeds that limit.

    Args:
        identifiers: A list of identifier values (e.g. email addresses
            or phone numbers) to look up.
        id_property: The HubSpot property name to match against
            (e.g. ``"email"`` or ``"phone"``). Must be a unique
            identifier property on the contact object.

    Returns:
        A list of contact result dicts returned by HubSpot.  Each dict
        contains at minimum ``"id"`` and a ``"properties"`` sub-dict
        with the matched identifier value.
    """
    payload = {
        "idProperty": id_property,
        "inputs": [{"id": value} for value in identifiers],
        "properties": [id_property],
    }
    response = requests.post(
        BATCH_URL,
        json=payload,
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    return response.json().get("results", [])


def retrieve_contacts(
    limit: int = 100,
    after: Optional[str] = None,
    properties: Optional[list[str]] = None,
) -> tuple[list[dict], str]:
    """Retrieve contacts from HubSpot with pagination and property selection.

    Args:
        limit: The maximum number of contacts to retrieve per page.
        after: The cursor to retrieve contacts after.
        properties: List of property names to fetch (e.g. ['email', 'phone']).

    Returns:
        A tuple of (list of contact dicts, next cursor).
    """
    params: dict[str, str | int] = {"limit": limit}
    if after:
        params["after"] = after
    if properties:
        params["properties"] = ",".join(properties)

    response = requests.get(
        BASE_URL,
        params=params,
        headers=_headers(),
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()
    return (
        data.get("results", []),
        data.get("paging", {}).get("next", {}).get("after", ""),
    )
