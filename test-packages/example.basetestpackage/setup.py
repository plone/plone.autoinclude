from setuptools import setup


setup(
    name="example.basetestpackage",
    version="1.0a1",
    description="Base test package for examples in plone.autoinclude",
    long_description="This package contains code that the other packages use for testing.",
    author="Maurits van Rees",
    author_email="m.van.rees@zestsoftware.nl",
    license="GPL version 2",
    include_package_data=True,
    zip_safe=False,
    extras_require={"z3c": ["z3c.autoinclude"]},
    # Note: no entry points here.
)
