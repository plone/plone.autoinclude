from .base_integration import IntegrationTestCase

import unittest


class TestIntegration(IntegrationTestCase, unittest.TestCase):
    project_name = "example.zopeintegration"
    target = "zope"
    meta_files = {
        "example.zopeintegration": ["meta.zcml"],
        "plone.autoinclude": ["meta.zcml"],
    }
    configure_files = {
        "example.zopeintegration": ["configure.zcml"],
    }
    overrides_files = {
        "example.zopeintegration": ["overrides.zcml"],
    }
    features = [
        "disable-autoinclude",
        "zopeintegration",
    ]
