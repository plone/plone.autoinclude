import unittest


class TestLoader(unittest.TestCase):
    def test_load_packages(self):
        from plone.autoinclude.loader import load_packages

        packages = load_packages()
        self.assertEqual(sorted(packages.keys()), ["example.ploneaddon"])
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

        context = None  # TODO: proper context
        self.assertIsNone(
            load_zcml_file(context, "zope.configuration", "zope.configuration")
        )
        self.assertIsNone(
            load_zcml_file(
                context, "zope.configuration", "zope.configuration", zcml="foo.zcml"
            )
        )
        self.assertIsNone(
            load_zcml_file(
                context, "zope.configuration", "zope.configuration", override=True
            )
        )
