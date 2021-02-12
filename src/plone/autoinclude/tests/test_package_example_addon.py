from .base import PackageTestCase

import unittest


class TestPackage(unittest.TestCase, PackageTestCase):
    project_name = "example.addon"
    features = ["addon"]
