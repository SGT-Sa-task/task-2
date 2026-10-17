"""
tests/test_phone_utils.py — Tests for VN phone normalization and validation.
"""

import pytest

from core.phone_utils import is_valid_vn_phone, normalize_vn_phone


@pytest.mark.parametrize(
    ("raw_phone", "expected"),
    [
        # Domestic format with leading '0'
        ("0901234567", "+84901234567"),
        ("0912345678", "+84912345678"),
        ("0328888999", "+84328888999"),
        ("0567123456", "+84567123456"),
        ("0701122334", "+84701122334"),
        ("0868999888", "+84868999888"),
        ("0888999000", "+84888999000"),
        ("0591234567", "+84591234567"),
        # Format with country code '+84'
        ("+84901234567", "+84901234567"),
        ("+84360000003", "+84360000003"),
        ("+84791234567", "+84791234567"),
        # Format with country code '84' (without '+')
        ("84901234567", "+84901234567"),
        ("84328888999", "+84328888999"),
        # Format without leading '0' or country code
        ("901234567", "+84901234567"),
        ("328888999", "+84328888999"),
        # Numbers containing whitespace, hyphens, dots
        ("090 123 4567", "+84901234567"),
        ("090-123-4567", "+84901234567"),
        ("090.123.4567", "+84901234567"),
        ("+84 (90) 123-4567", "+84901234567"),
    ],
)
def test_normalize_vn_phone_valid(raw_phone, expected):
    """Should accurately normalize valid Vietnamese phone numbers to '+84...'."""
    assert normalize_vn_phone(raw_phone) == expected
    assert is_valid_vn_phone(raw_phone) is True


@pytest.mark.parametrize(
    "invalid_phone",
    [
        "",
        None,
        "   ",
        "abc1234567",
        "1234567890",  # Invalid prefix (starts with 1)
        "0283812345",  # Landline number (not mobile)
        "09012345",  # Too short (8 digits)
        "090123456789",  # Too long (12 digits)
        "0401234567",  # Non-existent mobile prefix
        "+14155552671",  # US phone number
    ],
)
def test_normalize_vn_phone_invalid(invalid_phone):
    """Should return None and False for invalid or non-VN mobile phone numbers."""
    assert normalize_vn_phone(invalid_phone) is None
    assert is_valid_vn_phone(invalid_phone) is False
