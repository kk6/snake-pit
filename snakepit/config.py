# -*- coding: utf-8 -*-
import copy
import os

import click
import yaml

from . import exceptions

DEFAULT_CONFIG = {
    'default': 'requirements.in',
}


def get_config(config_path):
    """Return pit.yml data.

    :param config_path: YAML file name

    """
    if not os.path.exists(config_path):
        raise exceptions.ConfigDoesNotExist(
            "Config file not found: '{}'".format(config_path)
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


def get_requirements_file(config, requirement_path, name, mode='r'):
    if not requirement_path:
        if not name:
            name = 'default'
        try:
            requirement_path = config[name]
        except KeyError:
            raise exceptions.RequirementsKeyError(
                "Key not found in config: {}".format(name)
            )
    return click.open_file(requirement_path, mode)
