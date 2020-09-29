# -*- coding: utf-8 -*-
"""Installer for the plone.autoinclude package."""

from setuptools import find_packages, setup


setup(
    name="plone.autoinclude",
    version="1.0.0a1",
    description="Auto include code and zcml",
    # long_description: see metadata in setup.cfg
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="Maurits van Rees",
    author_email="maurits@vanrees.org",
    url="https://github.com/collective/plone.autoinclude",
    project_urls={
        "PyPI": "https://pypi.org/project/plone.autoinclude/",
        "Source": "https://github.com/plone/plone.autoinclude",
        "Tracker": "https://github.com/plone/plone.autoinclude/issues",
        # 'Documentation': 'https://plone.autoinclude.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["plone"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires="~=3.6",
    install_requires=[
        "setuptools",
    ],
    extras_require={
        # 'test': [
        #     # Maybe
        #     'plone.testing>=5.0.0',
        # ],
    },
    # Just as a reminder of a z3c.autoinclude entry point:
    # entry_points="""
    # [z3c.autoinclude.plugin]
    # target = plone
    # """,
)
