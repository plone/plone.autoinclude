from pkg_resources import iter_entry_points, resource_filename
from zope.configuration.xmlconfig import include, includeOverrides

import importlib
import logging
import os


logger = logging.getLogger(__name__)


# Dictionary of project names and packages that we have already imported.
_known_module_names = {}


def load_z3c_packages(target=""):
    """Load packages from the z3c.autoinclude.plugin entry points.

    After running the function, the packages have been imported.
    This returns a dictionary of package names and packages.
    """
    dists = {}
    for ep in iter_entry_points(group="z3c.autoinclude.plugin"):
        # If we look for target 'plone' then only consider entry points
        # that are registered for this target (module name).
        # But if the entry point is not registered for a specific target,
        # we can include it.
        if target and ep.module_name != target:
            continue
        module_name = ep.dist.project_name
        if module_name not in _known_module_names:
            try:
                dist = importlib.import_module(module_name)
            except ModuleNotFoundError:
                # Note: this may happen a lot, at least for z3c.autoinclude,
                # because the project name may not be the same as the package/module.
                logger.exception(f"Could not import {module_name}.")
                _known_module_names[module_name] = None
                continue
            _known_module_names[module_name] = dist
        dist = _known_module_names[module_name]
        if dist is not None:
            dists[module_name] = dist
    return dists


def load_own_packages(target=""):
    """Load packages from the plone.autoinclude.plugin entry points.

    After running the function, the packages have been imported.
    This returns a dictionary of package names and packages.

    Okay, entry points are less flexible than I thought.
    I expected you could write something like this:

        [plone.autoinclude]
        target = plone
        module = collective.mypackage
        zcml = configure.zcml,overrides.zcml

    and then you should be able to ask the entry point what its
    target, module and zcml attributes are.
    But this is not the case.
    You can only have one option in there, the rest is ignored.
    So either you set a target, or a module, or zcml.

    With 'target = plone' the entry point has name='target'
    and module_name='plone'.
    Calling entrypoint.load() will load the plone module.

    For our use case, it seems best to support target and module.

    - If the entrypoint names a target, then we use this as filter
      and assume the module name is the same as the package name.

    - If the entrypoint names a module, then we do not filter
      on target, but we load the module by the given name.
    """
    dists = {}
    for ep in iter_entry_points(group="plone.autoinclude.plugin"):
        # If we look for target 'plone' then only consider entry points
        # that are registered for this target (module name).
        # But if the entry point is not registered for a specific target,
        # we can include it.
        # import pdb; pdb.set_trace()
        module_name = None
        if ep.name == "target":
            if target and ep.module_name != target:
                # entry point defines target X but we only want target Y.
                continue
            module_name = ep.dist.project_name
        elif ep.name == "module":
            # We could load the dist with ep.load(), but we do it differently.
            module_name = ep.module_name
        else:
            # We could log a warning, but really this is an error.
            raise ValueError(
                f"plone.autoinclude.plugin entry point with unknown name found. "
                f"Expected is 'target' or 'module', got {ep.name}. "
                f"Package is {ep.dist.project_name}, entry point is {ep}"
            )
        if module_name not in _known_module_names:
            # We could try/except ModuleNotFoundError, but this is an unexpected error.
            dist = importlib.import_module(module_name)
            _known_module_names[module_name] = dist
        else:
            dist = _known_module_names[module_name]
        dists[module_name] = dist
    return dists


def load_packages(target=""):
    """Load packages from the autoinclude entry points.

    After running the function, the packages have been imported.
    This returns a dictionary of package names and packages.
    """
    dists = load_own_packages(target=target)
    z3c_dists = load_z3c_packages(target=target)
    dists.update(z3c_dists)
    return dists


def get_zcml_file(module_name, zcml="configure.zcml"):
    try:
        filename = resource_filename(module_name, zcml)
    except ModuleNotFoundError:
        # Note: this may happen a lot, at least for z3c.autoinclude,
        # because the project name may not be the same as the package/module.
        logger.exception(f"Could not import {module_name}.")
        _known_module_names[module_name] = None
        return
    if not os.path.isfile(filename):
        return
    return filename


def load_zcml_file(
    context, module_name, package=None, zcml="configure.zcml", override=False
):
    filename = get_zcml_file(module_name, zcml)
    if not filename:
        return
    if package is None and context.package is not None:
        package = context.package
    if override:
        logger.info(f"Loading {module_name}:{zcml} from {filename} in override mode.")
        # The package as third argument seems not needed because we have an absolute file name.
        # But it *is* needed when that file loads other relative files.
        includeOverrides(context, filename, package)
    else:
        logger.info(f"Loading {module_name}:{zcml} from {filename}")
        include(context, filename, package)


def load_configure(context, filename, dists):
    logger.info(f"Loading {filename} files.")
    for module_name, package in dists.items():
        logger.debug(module_name)
        load_zcml_file(context, module_name, package, filename)


def load_overrides(context, filename, dists):
    logger.info(f"Loading {filename} files in override mode.")
    for module_name, package in dists.items():
        logger.debug(module_name)
        load_zcml_file(context, module_name, package, "overrides.zcml", override=True)
