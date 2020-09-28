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


# Get entry points.
# For now only the z3c.autoinclude ones.
# Use this to import the Python code, if possible.
_dists = {}
for ep in iter_entry_points(group="z3c.autoinclude.plugin"):
    project_name = ep.dist.project_name
    if project_name.startswith("plone"):
        logger.info("Ignoring {project_name} for now.")
        continue
    # TODO: catch ModuleNotFoundError
    _dists[project_name] = importlib.import_module(project_name)

pprint(list(_dists.items()))


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
        context = new_configuration_context(package)
    if override:
        includeOverrides(context, filename, package)
    else:
        include(context, filename, package)


for project_name, module in _dists.items():
    logger.info(project_name)
    meta = load_zcml_file(project_name, "meta.zcml")
    configure = load_zcml_file(project_name, "configure.zcml")
    overrides = load_zcml_file(project_name, "overrides.zcml")
