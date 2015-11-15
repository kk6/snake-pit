# -*- coding: utf-8 -*-
import pytest


def test_YamlFileNotFoundError():
    from snakepit.config import get_requirements_file
    from snakepit import exceptions
    with pytest.raises(exceptions.YamlFileNotFoundError):
        get_requirements_file(yml='test.yml')


def test_RequirementsFileNotFoundError():
    from snakepit.config import get_requirements_file
    from snakepit import exceptions
    with pytest.raises(exceptions.RequirementsFileNotFoundError):
        get_requirements_file(yml='tests/fixtures/yaml/req_file_not_found.yml')


def test_RequirementsKeyNotFound():
    from snakepit.config import get_requirements_file
    from snakepit import exceptions
    with pytest.raises(exceptions.RequirementsKeyNotFound):
        get_requirements_file(yml='tests/fixtures/yaml/no_match_keys.yml')


def test_DefaultKeyNotFound():
    from snakepit.config import get_requirements_file
    from snakepit import exceptions
    with pytest.raises(exceptions.DefaultKeyNotFound):
        get_requirements_file(yml='tests/fixtures/yaml/no_default.yml')