# -*- coding: utf-8 -*-
import copy
import os

import yaml

from . import exceptions

PIT_CONFIG = os.environ.get('PIT_CONFIG', 'pit.yml')
DEFAULT_CONFIG = {
    'default': 'requirements.in',
}


def get_config(config_path=PIT_CONFIG):
    """Return pit.yml data.

    :param config_path: YAML file name

    """
    if not os.path.exists(config_path):
        raise exceptions.ConfigDoesNotExist(
            "'{}' not found in this directory.".format(config_path)
        )

    with open(config_path, 'r') as f:
        try:
            yaml_data = yaml.safe_load(f)
        except yaml.parser.ParserError as e:
            raise exceptions.InvalidConfiguration(
                '{0} is not a valid YAML file: line {1}: {2}'.format(
                    config_path,
                    e.problem_mark.line,
                    e.problem,
                )
            )
    config = copy.copy(DEFAULT_CONFIG)
    config.update(yaml_data)

    return config


def get_requirements_path(config, name):
    if not name:
        name = 'default'
    try:
        return config[name]
    except KeyError:
        raise exceptions.InvalidConfiguration(
            "Key not found in config: {}".format(name)
        )
