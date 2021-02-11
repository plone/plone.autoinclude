from .utils import get_configuration_context

import unittest


class TestLoader(unittest.TestCase):
    def test_load_packages(self):
        from plone.autoinclude.loader import load_packages

        packages = load_packages()
        self.assertEqual(
            sorted(packages.keys()), ["example.metaoverrides", "example.ploneaddon"]
        )
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
