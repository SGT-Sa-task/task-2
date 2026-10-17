"""
core/phone_utils.py — Utilities for validating and normalizing Vietnamese phone numbers.

Supported prefixes and carriers:
- 03x: Viettel (32-39)
- 05x: Vietnamobile (56, 58), Gmobile (59)
- 07x: Mobifone (70, 76-79)
- 08x: Vinaphone (81-85), Viettel (86), Vietnamobile (88), Gmobile (89)
- 09x: Viettel, Mobifone, Vinaphone (90-94, 96-99)
"""

import re
from typing import Optional

# Regex matches valid Vietnamese mobile numbers with
# or without country codes:
# Formats:
#   - 0901234567, 0321234567, ...
#   - 901234567, 321234567, ...
#   - 84901234567, +84901234567
VN_PHONE_REGEX = re.compile(
    r"^(\+84|84|0?)(3[2-9]|5[689]|7[06-9]|8[0-689]|9[0-46-9])([0-9]{7})$"
)


def normalize_vn_phone(raw_phone: Optional[str]) -> Optional[str]:
    """Validate and normalize a Vietnamese phone number to international '+84' format.

    Cleans spaces, hyphens, and dots, then matches against VN mobile network prefixes.

    Args:
        raw_phone: Raw phone string (e.g. '0901234567', '+84 901-234-567').

    Returns:
        Normalized phone string '+84xxxxxxxxx' if valid, or None if invalid or empty.
    """
    if not raw_phone:
        return None

    cleaned = str(raw_phone).strip()
    # Remove whitespace, dashes, dots, and parentheses
    cleaned = re.sub(r"[\s\-\.\(\)]", "", cleaned)

    match = VN_PHONE_REGEX.match(cleaned)
    if not match:
        return None

    _, prefix, suffix = match.groups()
    return f"+84{prefix}{suffix}"


def is_valid_vn_phone(raw_phone: Optional[str]) -> bool:
    """Check whether a given raw phone string is a valid Vietnamese mobile number.

    Args:
        raw_phone: Raw phone string.

    Returns:
        True if valid, False otherwise.
    """
    return normalize_vn_phone(raw_phone) is not None
