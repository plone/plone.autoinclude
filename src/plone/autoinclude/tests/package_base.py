from .utils import get_configuration_context
from importlib import import_module


class PackageTestCase:
    """Test our interaction with a package.

    You can find most packages in the test-packages directory in the repo.

    This is a base test class for all packages.
    You can inherit from this class and override the variables.

    The base class intentionally does not inherit unittest.TestCase,
    otherwise the test runner tries to run the tests from the base class as well.
    """

    project_name = ""
    # If module name differs from project name, fill this in:
    module_name = ""
    # Which files are included when we load meta.zcml, configure.zcml, overrides.zcml?
    # Make this empty in your test case when the package has no such zcml.
    # When you add a test package, make sure to update test_integration_plone.py
    # and maybe other integration tests as well: add the new package to
    # meta_files, configure_files and overrides_files there.
    meta_files = ["meta.zcml"]
    configure_files = ["configure.zcml"]
    overrides_files = ["overrides.zcml"]
    # Are any features provided when loading meta.zcml?
    features = []

    def import_me(self):
        if self.module_name:
            return import_module(self.module_name)
        return import_module(self.project_name)

    def test_load_packages(self):
        from plone.autoinclude.loader import load_packages

        packages = load_packages()
        if self.module_name:
            # Module name differs from project name.
            # Currently this means we cannot find any zcml.
            self.assertNotIn(self.project_name, packages.keys())
            self.assertNotIn(self.module_name, packages.keys())
            return

        self.assertIn(self.project_name, packages.keys())
        loaded_package = packages[self.project_name]
        imported_package = self.import_me()
        self.assertEqual(loaded_package, imported_package)

    def test_get_zcml_file_non_existing(self):
        from plone.autoinclude.loader import get_zcml_file

        self.assertIsNone(get_zcml_file(self.project_name, zcml="foo.zcml"))
        if self.module_name:
            self.assertIsNone(get_zcml_file(self.module_name, zcml="foo.zcml"))

    def test_get_zcml_file_default(self):
        from plone.autoinclude.loader import get_zcml_file

        if self.module_name:
            # The module name differs from the project name,
            # so getting the file by project name will fail.
            filename = get_zcml_file(self.project_name)
            self.assertIsNone(filename)
        filename = get_zcml_file(self.module_name or self.project_name)
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

    def test_load_zcml_file_meta(self):
        from plone.autoinclude.loader import load_zcml_file

        # prepare configuration context
        package = self.import_me()
        context = get_configuration_context(package)
        self.assertEqual(len(context._seen_files), 0)

        load_zcml_file(context, self.module_name or self.project_name, package, "meta.zcml")
        for filepath in self.meta_files:
            self.assertIn(context.path(filepath), context._seen_files)
        self.assertEqual(len(context._seen_files), len(self.meta_files))

        # meta.zcml may have a meta:provides option.
        for feature in self.features:
            self.assertTrue(
                context.hasFeature(feature), f"meta:provides feature {feature} missing"
            )
        self.assertEqual(context._features, set(self.features))

    def test_load_zcml_file_configure(self):
        from plone.autoinclude.loader import load_zcml_file

        # prepare configuration context
        package = self.import_me()
        context = get_configuration_context(package)
        self.assertEqual(context._features, set())

        # Load configure.zcml.
        load_zcml_file(context, self.module_name or self.project_name, package)
        for filepath in self.configure_files:
            self.assertIn(context.path(filepath), context._seen_files)
        self.assertEqual(len(context._seen_files), len(self.configure_files))

    def test_load_zcml_file_overrides(self):
        from plone.autoinclude.loader import load_zcml_file

        package = self.import_me()
        context = get_configuration_context(package)
        load_zcml_file(
            context, self.module_name or self.project_name, package, "overrides.zcml", override=True
        )
        for filepath in self.overrides_files:
            self.assertIn(context.path(filepath), context._seen_files)
        self.assertEqual(len(context._seen_files), len(self.overrides_files))

    def test_load_zcml_file_non_existing(self):
        from plone.autoinclude.loader import load_zcml_file

        package = self.import_me()
        context = get_configuration_context(package)
        load_zcml_file(context, self.module_name or self.project_name, package, zcml="non_existing.zcml")
        self.assertEqual(len(context._seen_files), 0)
