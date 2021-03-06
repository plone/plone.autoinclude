from plone.autoinclude.tests.package_base import PackageTestCase

import unittest


class TestPackage(PackageTestCase, unittest.TestCase):
    project_name = "example.metaoverrides"
    # This package only has meta.zcml and overrides.zcml, no configure.zcml.
    configure_files = []
    features = ["metaoverrides"]
