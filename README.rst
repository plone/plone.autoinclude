.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.org/plone/plone.autoinclude.svg?branch=master
    :target: https://travis-ci.org/plone/plone.autoinclude

.. image:: https://coveralls.io/repos/github/plone/plone.autoinclude/badge.svg?branch=master
    :target: https://coveralls.io/github/plone/plone.autoinclude?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/v/plone.autoinclude.svg
    :target: https://pypi.python.org/pypi/plone.autoinclude/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/plone.autoinclude.svg
    :target: https://pypi.python.org/pypi/plone.autoinclude
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/plone.autoinclude.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/plone.autoinclude.svg
    :target: https://pypi.python.org/pypi/plone.autoinclude/
    :alt: License


=================
plone.autoinclude
=================

Tell me what your product does

Features
--------

- See https://github.com/plone/Products.CMFPlone/issues/3053
- An alternative to ``z3c.autoinclude``.
- When a package registers an autoinclude entry point, we load its Python code at Zope/Plone startup.
- And we load its zcml.
- Works with Buildout-installed packages.
- Works with pip-installed packages.


Compatibility
-------------

This is made for Python 3.6+.


Installation
------------

Install plone.autoinclude by adding it to your buildout::

    [buildout]

    ...

    eggs =
        plone.autoinclude
    zcml =
        plone.autoinclude-meta


and then running ``bin/buildout``

For core Plone my intention would be to do this:

- In ``Products.CMFPlone/meta.zcml`` set::

    <include package="plone.autoinclude" file="meta.zcml" />
    <autoIncludePlugins target="plone" file="meta.zcml" />

- In ``Products.CMFPlone/configure.zcml`` set::

    <autoIncludePlugins target="plone" file="configure.zcml" />

- In ``Products.CMFPlone/overrides.zcml`` set::

    <autoIncludePluginsOverrides target="plone" file="overrides.zcml" />

See also the ``package-includes`` directory in this repository.
And see `CMFPlone branch plone-autoinclude <https://github.com/plone/Products.CMFPlone/tree/plone-autoinclude>`_, based on 5.2.x.


Installation with pip
---------------------

Let's leave buildout completely out of the picture and only use pip::

    # Create virtual environment in the current directory:
    python3.8 -mvenv .
    # Install Plone:
    bin/pip install -c https://dist.plone.org/release/5.2.3/constraints3.txt Products.CMFPlone
    # Install plone.autoinclude from the current git checkout:
    bin/pip install -e .
    # When I try bin/mkwsgiinstance it complains that Paste is missing.
    # We could use waitress instead, but let's try Paste for now:
    bin/pip install -c https://dist.plone.org/release/5.2.3/constraints3.txt Paste
    # Create the Zope WSGI instance:
    bin/mkwsgiinstance -d . -u admin:admin
    # Copy our zcml that disables z3c.autoinclude and enables our own:
    cp -a package-includes etc/
    # Start Zope:
    bin/runwsgi -v etc/zope.ini


Contribute
----------

- Issue Tracker: https://github.com/plone/plone.autoinclude/issues
- Source Code: https://github.com/plone/plone.autoinclude


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
