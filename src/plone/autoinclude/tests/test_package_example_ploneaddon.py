from .base import PackageTestCase

import unittest


class TestPackage(unittest.TestCase, PackageTestCase):
    project_name = "example.ploneaddon"
    meta_files = []
    configure_files = ["configure.zcml", "permissions.zcml", "browser/configure.zcml"]
    overrides_files = []
