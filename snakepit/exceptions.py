# -*- coding: utf-8 -*-

from ._compat import FileNotFoundError


class SnakePitException(Exception):
    """Base exception class"""


class ConfigDoesNotExist(SnakePitException, FileNotFoundError):
    """Raised when config file not found."""


class InvalidConfiguration(SnakePitException):
    """Raised when does not open config file."""


class RequirementsKeyError(SnakePitException, KeyError):
    """Raised when key not found in config file."""


class DistributionNotFound(SnakePitException):
    """Raised when distribution not found."""
