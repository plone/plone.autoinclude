from setuptools import setup


setup(
    name="example.different2",
    version="1.0a1",
    description="A second different package which is actually something else too",
    long_description="Package name differs from import module name, using new entry point.",
    author="Maurits van Rees",
    author_email="m.van.rees@zestsoftware.nl",
    license="GPL version 2",
    include_package_data=True,
    zip_safe=False,
    entry_points="""
    [plone.autoinclude.plugin]
    module = example.somethingelse2
    """,
)
