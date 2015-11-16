# -*- coding: utf-8 -*-

from ._compat import FileNotFoundError


class ConfigDoesNotExist(FileNotFoundError):
    """Raised when config file not found."""


class InvalidConfiguration(Exception):
    """Raised when does not open config file"""
