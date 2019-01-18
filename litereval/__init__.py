from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .__main__ import (
    litereval, merge, args_kwargs, get_args,
    LiterEvalError, tuple_, validated, get
)
