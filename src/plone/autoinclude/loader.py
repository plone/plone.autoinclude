from pkg_resources import iter_entry_points
from pkg_resources import resource_filename
from pprint import pprint
from zope.configuration.xmlconfig import include
from zope.configuration.xmlconfig import includeOverrides

import importlib
import logging
import os


logger = logging.getLogger(__name__)


# Dictionary with distributions/module.
# Key is project name, value is imported module.
# I'm not yet sure if we need the module.
_dists = {}


def load_packages(target=""):
    """Load packages from the autoinclude entry points.

    For now we only get the z3c.autoinclude entry points,
    for backwards compatibility.
    I want entry points of our own as well.

    After running the function, the packages have been imported.
    """
    global _dists
    for ep in iter_entry_points(group="z3c.autoinclude.plugin"):
        if target and ep.module_name != target:
            continue
        project_name = ep.dist.project_name
        if project_name.startswith("plone"):
            # It takes quite a while to import all these packages.
            logger.info(f"Ignoring {project_name} for now.")
            continue
        if project_name in _dists:
            # already loaded
            continue
        # TODO: catch ModuleNotFoundError.  But for now I want to see this error.
        _dists[project_name] = importlib.import_module(project_name)


def get_zcml_file(project_name, zcml="configure.zcml"):
    filename = resource_filename(project_name, zcml)
    if not os.path.isfile(filename):
        return
    return filename


def load_zcml_file(context, project_name, zcml="configure.zcml", override=False):
    filename = get_zcml_file(project_name, zcml)
    if not filename:
        return
    global _dists
    package = _dists[project_name]
    if override:
        logger.info(f"Loading {project_name}:{filename} in override mode.")
        includeOverrides(context, filename, package)
    else:
        logger.info(f"Loading {project_name}:{filename}.")
        include(context, filename, package)


def load_configure(context, filename):
    logger.info(f"Loading {filename} files.")
    global _dists
    for project_name in _dists.keys():
        logger.info(project_name)
        load_zcml_file(context, project_name, filename)


def load_overrides(context, filename):
    logger.info(f"Loading {filename} files in override mode.")
    global _dists
    for project_name in _dists.keys():
        logger.info(project_name)
        load_zcml_file(context, project_name, "overrides.zcml", override=True)
