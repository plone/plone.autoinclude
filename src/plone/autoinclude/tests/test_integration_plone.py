from .base_integration import IntegrationTestCase

import unittest


class TestIntegration(IntegrationTestCase, unittest.TestCase):
    project_name = "example.ploneintegration"
    target = "plone"
    meta_files = {
        "example.ploneintegration": ["meta.zcml"],
        "plone.autoinclude": ["meta.zcml"],
        "example.metaoverrides": ["meta.zcml"],
    }
    configure_files = {
        "example.ploneintegration": ["configure.zcml"],
        "example.ploneaddon": [
            "configure.zcml",
            "permissions.zcml",
            "browser/configure.zcml",
        ],
    }
    overrides_files = {
        "example.ploneintegration": ["overrides.zcml"],
        "example.metaoverrides": ["overrides.zcml"],
    }
    features = [
        "disable-autoinclude",
        "metaoverrides",
        "ploneintegration",
    ]
