from . import loader
from zope.interface import Interface
from zope.configuration.xmlconfig import include, includeOverrides
from zope.configuration.fields import GlobalObject
from zope.dottedname.resolve import resolve
from zope.schema import NativeStringLine

# from z3c.autoinclude import api

import logging


logger = logging.getLogger(__name__)


class IIncludePluginsDirective(Interface):
    """Auto-include any ZCML in the dependencies of this package."""

    package = NativeStringLine(
        title=u"Package to auto-include for",
        description=u"""
        Auto-include all plugins to this package.
        """,
        # Note: z3c.autoinclude has required=True
        required=False,
    )

    file = NativeStringLine(
        title=u"ZCML filename to look for",
        description=u"""
        Name of a particular ZCML file to look for.
        If omitted, autoinclude will scan for standard filenames
        (e.g. meta.zcml, configure.zcml, overrides.zcml)
        """,
        required=False,
    )


def includePluginsDirective(context, package, file=None):

    # if api.plugins_disabled():
    #     log.warn(
    #         "z3c.autoinclude.plugin is disabled but is being invoked by %s"
    #         % _context.info
    #     )
    #     return

    if file is None:
        zcml_to_look_for = ["meta.zcml", "configure.zcml"]
    else:
        zcml_to_look_for = [file]

    # TODO: get list of packages back?
    loader.load_packages(package)

    for filename in zcml_to_look_for:
        loader.load_configure(context, filename)


def includePluginsOverridesDirective(context, package, file=None):

    # if api.plugins_disabled():
    #     log.warn(
    #         "z3c.autoinclude.plugin is disabled but is being invoked by %s"
    #         % _context.info
    #     )
    #     return

    if file is None:
        zcml_to_look_for = ["overrides.zcml"]
    else:
        zcml_to_look_for = [file]
    loader.load_packages(package)

    for filename in zcml_to_look_for:
        loader.load_configure(context, filename)
