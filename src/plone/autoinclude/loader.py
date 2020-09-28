from pkg_resources import iter_entry_points
from pkg_resources import resource_filename
from pprint import pprint
from zope.configuration.config import ConfigurationMachine
from zope.configuration.xmlconfig import include
from zope.configuration.xmlconfig import includeOverrides
from zope.configuration.xmlconfig import registerCommonDirectives

import importlib
import logging
import os


logger = logging.getLogger(__name__)


def new_configuration_context(package):
    # We need a configuration context for our code.
    # We should probably use an already existing one,
    # but for testing I guess we can create our own.
    context = ConfigurationMachine()
    registerCommonDirectives(context)
    context.package = package
    return context


# Dictionary with distributions/module.
# Key is project name, value is imported module.
# I'm not yet sure if we need the module.
_dists = {}


def load_packages():
    """Load packages from the autoinclude entry points.

    For now we only get the z3c.autoinclude entry points,
    for backwards compatibility.
    I want entry points of our own as well.

    After running the function, the packages have been imported.
    """
    for ep in iter_entry_points(group="z3c.autoinclude.plugin"):
        project_name = ep.dist.project_name
        if project_name.startswith("plone"):
            # It takes quite a while to import all these packages.
            logger.info("Ignoring {project_name} for now.")
            continue
        # TODO: catch ModuleNotFoundError.  But for now I want to see this error.
        _dists[project_name] = importlib.import_module(project_name)


def get_zcml_file(project_name, zcml="configure.zcml"):
    filename = resource_filename(project_name, zcml)
    if not os.path.isfile(filename):
        return
    return filename


def load_zcml_file(project_name, zcml="configure.zcml", override=False, context=None):
    filename = get_zcml_file(project_name, zcml)
    if not filename:
        return
    global _dists
    package = _dists[project_name]
    if context is None:
        # XXX This does not really work for me.  Sample error:
        # zope.configuration.exceptions.ConfigurationError:
        # ('Unknown directive', 'http://namespaces.zope.org/i18n', 'registerTranslations')
        context = new_configuration_context(package)
    if override:
        logger.info("Loading {project_name}:{filename} in override mode.")
        includeOverrides(context, filename, package)
    else:
        logger.info("Loading {project_name}:{filename}.")
        include(context, filename, package)


def load_meta():
    logger.info("Loading meta .zcml files.")
    global _dists
    for project_name, module in _dists.items():
        logger.info(project_name)
        meta = load_zcml_file(project_name, "meta.zcml")


def load_configure():
    logger.info("Loading configure.zcml files.")
    global _dists
    for project_name, module in _dists.items():
        logger.info(project_name)
        configure = load_zcml_file(project_name, "configure.zcml")


def load_overrides():
    logger.info("Loading overrides.zcml files.")
    global _dists
    for project_name, module in _dists.items():
        logger.info(project_name)
        overrides = load_zcml_file(project_name, "overrides.zcml", override=True)
