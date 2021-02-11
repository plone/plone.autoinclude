from copy import copy
import os
import sys
import pkg_resources
from setuptools.command.egg_info import egg_info
import distutils.core
from .base import PackageTestCase

import unittest


class TestPackage(unittest.TestCase, PackageTestCase):
    project_name = "example.ploneaddon"
    meta_files = []
    configure_files = ["configure.zcml", "permissions.zcml", "browser/configure.zcml"]
    overrides_files = []

    def setUp(self):
        workingset = pkg_resources.working_set
        self.workingdir = os.getcwd()
        self.stored_syspath = copy(sys.path)
        projects_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'test-packages')  # noqa: E501
        test_packages = os.listdir(projects_dir)
        self.added_entries = []
        for package in test_packages:
            packagedir = os.path.join(projects_dir, package)
            os.chdir(packagedir)
            dist = distutils.core.run_setup('setup.py')
            ei = egg_info(dist)
            ei.finalize_options()
            try:
                os.mkdir(ei.egg_info)
            except FileExistsError:
                pass
            ei.run()
            egginfodir = os.path.join(packagedir, 'src')
            workingset.add_entry(egginfodir)
            self.added_entries.append(egginfodir)
            sys.path.append(egginfodir)
        os.chdir(self.workingdir)

    def tearDown(self):
        os.chdir(self.workingdir)
        sys.path = self.stored_syspath
        workingset = pkg_resources.working_set
        for entry in self.added_entries:
            workingset.entries.remove(entry)
