from setuptools import setup


setup(
    name="example.metaoverrides",
    version="1.0a1",
    description="An add-on for Plone",
    long_description="long_description",
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
