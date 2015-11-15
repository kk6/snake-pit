# -*- coding: utf-8 -*-

from ._compat import FileNotFoundError


class YamlFileNotFoundError(FileNotFoundError):
    """Raised when yaml file not found."""


class RequirementsFileNotFoundError(FileNotFoundError):
    """Raised when specified requirements file not found."""


class RequirementsKeyNotFound(Exception):
    """Raised when 'requirements' key not found in yaml"""


class DefaultKeyNotFound(Exception):
    """Raised when default requirements's path name in yaml.

    You must specify a default in one of the following ways.

        1. set 'default' hash in yaml.
        2. Specify the 'default' hash as a child element of 'requirements' key of yaml.

    """
