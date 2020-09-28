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
