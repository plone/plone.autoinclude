from importlib import import_module

import unittest


class TestPackagePloneAddon(unittest.TestCase):
    """Test our interaction with the example.ploneaddon package.

    You can find this package in the test-packages directory in the repo.
    We may want to create a base test class for all packages.
    But we start with one.
    """

    project_name = "example.ploneaddon"
    # How many files are loaded when we load meta.zcml, configure.zcml, overrides.zcml?
    meta_files = 0
    configure_files = 3
    overrides_files = 0

    def test_load_packages(self):
        from plone.autoinclude.loader import load_packages

        packages = load_packages()
        self.assertIn(self.project_name, packages.keys())
        loaded_package = packages[self.project_name]
        imported_package = import_module(self.project_name)
        self.assertEqual(loaded_package, imported_package)

    def test_get_zcml_file_non_existing(self):
        from plone.autoinclude.loader import get_zcml_file

        self.assertIsNone(get_zcml_file(self.project_name, zcml="foo.zcml"))

    def test_get_zcml_file_default(self):
        from plone.autoinclude.loader import get_zcml_file

        filename = get_zcml_file(self.project_name)
        if not self.configure_files:
            self.assertIsNone(filename)
            return
        self.assertIsNotNone(filename)
        with open(filename) as myfile:
            self.assertIn(
                f"This is configure.zcml from {self.project_name}.", myfile.read()
            )

    def _context(self, package=None):
        # Various functions take a configuration context as argument.
        # From looking at zope.configuration.xmlconfig.file the following seems about right.
        from zope.configuration.config import ConfigurationMachine
        from zope.configuration.xmlconfig import registerCommonDirectives

        context = ConfigurationMachine()
        registerCommonDirectives(context)
        if package is not None:
            # When you set context.package, context.path(filename) works nicely.
            context.package = package
        return context

    def test_load_zcml_file_configure(self):
        from plone.autoinclude.loader import load_zcml_file

        # prepare configuration context
        package = import_module(self.project_name)
        context = self._context(package)
        self.assertEqual(len(context._seen_files), 0)

        # Load configure.zcml.
        load_zcml_file(context, self.project_name, package)
        self.assertEqual(len(context._seen_files), self.configure_files)
        self.assertIn(context.path("configure.zcml"), context._seen_files)
        # This includes two other files.
        self.assertIn(context.path("permissions.zcml"), context._seen_files)
        self.assertIn(context.path("browser/configure.zcml"), context._seen_files)

    def test_load_zcml_file_non_existing(self):
        from plone.autoinclude.loader import load_zcml_file

        package = import_module(self.project_name)
        context = self._context(package)
        load_zcml_file(context, self.project_name, package, zcml="foo.zcml")
        self.assertEqual(len(context._seen_files), 0)

    def test_load_zcml_file_overrides(self):
        from plone.autoinclude.loader import load_zcml_file

        package = import_module(self.project_name)
        context = self._context(package)
        # currently we have no override
        load_zcml_file(
            context, self.project_name, package, "overrides.zcml", override=True
        )
        self.assertEqual(len(context._seen_files), self.overrides_files)
