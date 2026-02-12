from setuptools import setup


setup(
    name="example.multipleeps",
    version="1.0a1",
    description="An add-on for Plone",
    long_description="long_description",
    author="Thomas Schorr",
    author_email="t_schorr@gmx.de",
    license="GPL version 2",
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "z3c.autoinclude.plugin": [
            "dummy = dummy",
        ],
        "plone.autoinclude.plugin": [
            "target = plone",
            "module = example.multipleeps",
        ],
    },
)
