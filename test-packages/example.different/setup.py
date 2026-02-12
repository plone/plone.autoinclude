from setuptools import setup


setup(
    name="example.different",
    version="1.0a1",
    description="A different package which is actually something else",
    long_description="Package name differs from import module name",
    author="Maurits van Rees",
    author_email="m.van.rees@zestsoftware.nl",
    license="GPL version 2",
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
