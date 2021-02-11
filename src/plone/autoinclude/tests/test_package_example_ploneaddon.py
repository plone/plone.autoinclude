from .base import PackageTestCase

import unittest


class TestPackagePloneAddon(unittest.TestCase, PackageTestCase):
    """Test our interaction with the example.ploneaddon package.

    You can find this package in the test-packages directory in the repo.
    """

    project_name = "example.ploneaddon"
    meta_files = []
    configure_files = ["configure.zcml", "permissions.zcml", "browser/configure.zcml"]
    overrides_files = []
