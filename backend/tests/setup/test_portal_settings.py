"""Portal settings tests."""
from plone import api

import pytest


class TestPortalSettings:
    """Test that Portal configuration is correctly done."""

    @pytest.mark.parametrize(
        "key,expected",
        [
            ["plone.site_title", "Portal de Governo do RS"],
            ["plone.email_from_name", "Portal de Governo do RS"],
            ["plone.smtp_host", "localhost"],
            ["plone.smtp_port", 25],
        ],
    )
    def test_setting(self, portal, key: str, expected: str):
        """Test portal title."""
        value = api.portal.get_registry_record(key)
        assert value == expected
