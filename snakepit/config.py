# -*- coding: utf-8 -*-
import os

import yaml

from . import exceptions
from ._compat import FileNotFoundError

PIT_CONFIG = os.environ.get('PIT_CONFIG', 'pit.yml')


def get_yaml_data(filename=PIT_CONFIG):
    """Return pit.yml data.

    :param filename: YAML file name
    """
    with open(filename, 'r') as f:
        return yaml.load(f)


def get_requirements_file(requirements_key=None, yml=PIT_CONFIG, mode='r'):
    """Return requirements file path from yaml.

    :param requirements_key: requirements key.
    :param yml: YAML file name.
    :param mode: File opening mode.

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
