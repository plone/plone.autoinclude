from plone.autoinclude.tests.package_base import PackageTestCase

import unittest


class TestPackage(PackageTestCase, unittest.TestCase):
    project_name = "example.different"
    module_name = "example.somethingelse"
    features = ["different"]
