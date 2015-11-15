# -*- coding: utf-8 -*-

import yaml

from . import exceptions
from ._compat import FileNotFoundError

YAML_FILE = 'pit.yml'


def get_yaml_data(filename=YAML_FILE):
    """Return pit.yml data."""
    with open(filename, 'r') as f:
        return yaml.load(f)


def get_requirements_file(requirements_key=None, yml=YAML_FILE, mode='r'):
    """Return requirements file path from yaml.

    :param requirements_key: requirements key.

    """
    try:
        data = get_yaml_data(yml)
    except (FileNotFoundError, IOError):
        raise exceptions.YamlFileNotFoundError(
            "'pit.yml' not found in this directory.")

    if requirements_key:
        pass
    elif 'default' in data:
        requirements_key = data['default']
    else:
        requirements_key = 'default'

    try:
        req = data['requirements']
    except KeyError:
        raise exceptions.RequirementsKeyNotFound(
            "'requirement' key must be required in 'pit.yml'")

    try:
        requirements_path = req[requirements_key]
    except KeyError:
        raise exceptions.DefaultKeyNotFound(
            "Default requirements key not found in 'pit.yml'"
        )
    else:
        try:
            requirements_file = open(requirements_path, mode)
        except (FileNotFoundError, IOError):
            raise exceptions.RequirementsFileNotFoundError(
                "Requirements file not found: {}".format(requirements_path))
        else:
            return requirements_file
