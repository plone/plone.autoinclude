TODO
----

Next to supporting old-style z3c.autoinclude entry points, make our own.
See some `variants in issue 3053 <https://github.com/plone/Products.CMFPlone/issues/3053#issuecomment-669156028>`_.
This is especially needed for cases where there is a difference between package name, project name, dotted name, module name, whatever.
It also gives the packages more flexibility:
for example only load ``configure.zcml`` and not ``overrides.zcml``.

This very much needs tests.
Certainly unit tests.
We can get inspiration from z3c.autoinclude, see for example the sample packages that are in itstests directory.

We should also create some Github Actions or similar to try a few common scenarios:

- Install Plone with Buildout and start the instance.
- Install Plone with pip, use ``bin/mkwsgiinstance`` and start the instance.
- Install Plone with pip and then run Buildout and start the instance.

