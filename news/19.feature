Raise an exception when a module is not found.
When environment variable ``AUTOINCLUDE_ALLOW_MODULE_NOT_FOUND_ERROR=1`` is set, we log an error and continue.
To accept ``ModuleNotFoundError`` only in specific packages, use a comma-separated list of project names, with or without spaces.
See `issue 19 <https://github.com/plone/plone.autoinclude/issues/19>`_.
[maurits]
