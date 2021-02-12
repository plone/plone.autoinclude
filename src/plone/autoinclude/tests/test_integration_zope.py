from plone.autoinclude.tests.integration_base import IntegrationTestCase

import unittest


class TestIntegration(IntegrationTestCase, unittest.TestCase):
    project_name = "example.zopeintegration"
    target = "zope"
    meta_files = {
        "example.zopeintegration": ["meta.zcml"],
        "example.zopeaddon": ["meta.zcml", "browser/meta.zcml"],
        "plone.autoinclude": ["meta.zcml"],
    }
    configure_files = {
        "example.zopeintegration": ["configure.zcml"],
        "example.zopeaddon": ["configure.zcml", "browser/configure.zcml"],
    }
    overrides_files = {
        "example.zopeintegration": ["overrides.zcml"],
        "example.zopeaddon": ["overrides.zcml", "browser/browser-overrides.zcml"],
    }
    features = [
        "disable-autoinclude",
        "zopeaddon",
        "zopeaddon-browser",
        "zopeintegration",
    ]
