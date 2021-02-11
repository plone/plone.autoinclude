from .base import PackageTestCase

import unittest


class TestPackagePloneAddon(unittest.TestCase, PackageTestCase):
    """Test our interaction with the example.ploneaddon package.

    You can find this package in the test-packages directory in the repo.
    """

    project_name = "example.ploneaddon"
    # How many files are loaded when we load meta.zcml, configure.zcml, overrides.zcml?
    meta_files = 0
    configure_files = 3
    overrides_files = 0
