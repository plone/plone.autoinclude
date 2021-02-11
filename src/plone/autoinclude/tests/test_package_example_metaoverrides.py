from .base import PackageTestCase

import unittest


class TestPackage(unittest.TestCase, PackageTestCase):
    project_name = "example.metaoverrides"
    # This package only has meta.zcml and overrides.zcml, no configure.zcml.
    configure_files = []
