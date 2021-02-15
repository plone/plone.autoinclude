from copy import copy
import os
import sys
import pkg_resources
from setuptools.command.egg_info import egg_info
import distutils.core
from .utils import get_configuration_context

import unittest


class TestLoader(unittest.TestCase):

    def setUp(self):
        workingset = pkg_resources.working_set
        self.workingdir = os.getcwd()
        self.stored_syspath = copy(sys.path)
        projects_dir = os.path.join(os.path.dirname(__file__), 'test-packages')  # noqa: E501
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

    def test_load_z3c_packages(self):
        from plone.autoinclude.loader import load_z3c_packages

        packages = load_z3c_packages()
        for package in ["example.ploneaddon", ]:
            self.assertIn(package, packages.keys())
        package = packages["example.ploneaddon"]
        import example.ploneaddon

        self.assertEqual(package, example.ploneaddon)

    def test_load_own_packages(self):
        from plone.autoinclude.loader import load_own_packages

        packages = load_own_packages()
        for package in ["example.ploneaddon", ]:
            self.assertIn(package, packages.keys())
        package = packages["example.ploneaddon"]
        import example.ploneaddon

        self.assertEqual(package, example.ploneaddon)

    def test_get_zcml_file(self):
        from plone.autoinclude.loader import get_zcml_file

        self.assertIsNone(get_zcml_file("zope.configuration"))
        self.assertIsNone(get_zcml_file("zope.configuration", zcml="foo.zcml"))
        filename = get_zcml_file("example.ploneaddon")
        self.assertIsNotNone(filename)
        with open(filename) as myfile:
            self.assertIn(
                "This is configure.zcml from example.ploneaddon.", myfile.read()
            )
        self.assertIsNone(get_zcml_file("example.ploneaddon", zcml="foo.zcml"))

    def test_load_zcml_file(self):
        from plone.autoinclude.loader import load_zcml_file

        import zope.configuration as package

        context = get_configuration_context(package)
        project_name = "zope.configuration"
        load_zcml_file(context, project_name, package)
        load_zcml_file(context, project_name, package, zcml="foo.zcml")
        load_zcml_file(context, project_name, package, "overrides.zcml", override=True)
