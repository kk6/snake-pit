# -*- coding: utf-8 -*-

from ._compat import FileNotFoundError


class ConfigDoesNotExist(FileNotFoundError):
    """Raised when config file not found."""


class InvalidConfiguration(Exception):
    """Raised when does not open config file."""


class RequirementsKeyError(KeyError):
    """Raised when key not found in config file."""


class DistributionNotFound(Exception):
    """Raised when distribution not found."""
