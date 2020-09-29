from pkg_resources import iter_entry_points
from pkg_resources import resource_filename
from pprint import pprint
from zope.configuration.xmlconfig import include
from zope.configuration.xmlconfig import includeOverrides

import importlib
import logging
import os


logger = logging.getLogger(__name__)


# Dictionary of project names and packages that we have already imported.
_known_project_names = {}


def load_packages(target=""):
    """Load packages from the autoinclude entry points.

    For now we only get the z3c.autoinclude entry points,
    for backwards compatibility.
    I want entry points of our own as well.

    After running the function, the packages have been imported.

    This returns a dictionary of package names and packages.
    """
    dists = {}
    for ep in iter_entry_points(group="z3c.autoinclude.plugin"):
        # If we look for target 'plone' then only consider entry points
        # that are registered for this target (module name).
        # But if the entry point is not registered for a specific target,
        # we can include it.
        if target and ep.module_name and ep.module_name != target:
            continue
        project_name = ep.dist.project_name
        # if project_name.startswith("plone"):
        #     # It takes quite a while to import all these packages.
        #     logger.info(f"Ignoring {project_name} for now.")
        #     continue
        if project_name not in _known_project_names:
            try:
                dist = importlib.import_module(project_name)
            except ModuleNotFoundError:
                # Note: this may happen a lot, at least for z3c.autoinclude,
                # because the project name may not be the same as the package/module.
                logger.exception(f"Could not import {project_name}.")
                _known_project_names[project_name] = None
                continue
            _known_project_names[project_name] = dist
        dist = _known_project_names[project_name]
        if dist is not None:
            dists[project_name] = dist
    return dists


def get_zcml_file(project_name, zcml="configure.zcml"):
    filename = resource_filename(project_name, zcml)
    if not os.path.isfile(filename):
        return
    return filename


def load_zcml_file(
    context, project_name, package, zcml="configure.zcml", override=False
):
    filename = get_zcml_file(project_name, zcml)
    if not filename:
        return
    if override:
        logger.info(f"Loading {project_name}:{filename} in override mode.")
        # The package as third argument seems not needed because we have an absolute file name.
        # But it *is* needed when that file loads other relative files.
        includeOverrides(context, filename, package)
    else:
        logger.info(f"Loading {project_name}:{filename}.")
        include(context, filename, package)


def load_configure(context, filename, dists):
    logger.info(f"Loading {filename} files.")
    for project_name, package in dists.items():
        logger.debug(project_name)
        load_zcml_file(context, project_name, package, filename)


def load_overrides(context, filename, dists):
    logger.info(f"Loading {filename} files in override mode.")
    for project_name, package in dists.items():
        logger.debug(project_name)
        load_zcml_file(context, project_name, package, "overrides.zcml", override=True)
