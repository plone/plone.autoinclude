from pkg_resources import iter_entry_points
from pkg_resources import resource_filename
from pprint import pprint
from zope.configuration.xmlconfig import include
from zope.configuration.xmlconfig import includeOverrides

import importlib
import logging
import os


logger = logging.getLogger(__name__)


# Set of project names that we have already imported.
_known_project_names = set()


def load_packages(target=""):
    """Load packages from the autoinclude entry points.

    For now we only get the z3c.autoinclude entry points,
    for backwards compatibility.
    I want entry points of our own as well.

    After running the function, the packages have been imported.

    This returns a set of package names.
    """
    dists = set()
    for ep in iter_entry_points(group="z3c.autoinclude.plugin"):
        if target and ep.module_name != target:
            continue
        project_name = ep.dist.project_name
        if project_name.startswith("plone"):
            # It takes quite a while to import all these packages.
            logger.info(f"Ignoring {project_name} for now.")
            continue
        if project_name not in _known_project_names:
            # TODO: catch ModuleNotFoundError.  But for now I want to see this error.
            importlib.import_module(project_name)
        dists.add(project_name)
    _known_project_names.union(dists)
    return dists


def get_zcml_file(project_name, zcml="configure.zcml"):
    filename = resource_filename(project_name, zcml)
    if not os.path.isfile(filename):
        return
    return filename


def load_zcml_file(context, project_name, zcml="configure.zcml", override=False):
    filename = get_zcml_file(project_name, zcml)
    if not filename:
        return
    if override:
        logger.info(f"Loading {project_name}:{filename} in override mode.")
        # We could pass a package or a dotted name as third argument,
        # but that seems not needed because we have an absolute file name.
        includeOverrides(context, filename)
    else:
        logger.info(f"Loading {project_name}:{filename}.")
        include(context, filename)


def load_configure(context, filename, dotted_names):
    logger.info(f"Loading {filename} files.")
    for project_name in dotted_names:
        logger.info(project_name)
        load_zcml_file(context, project_name, filename)


def load_overrides(context, filename, dotted_names):
    logger.info(f"Loading {filename} files in override mode.")
    for project_name in dotted_names:
        logger.info(project_name)
        load_zcml_file(context, project_name, "overrides.zcml", override=True)
