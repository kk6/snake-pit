# -*- coding: utf-8 -*-
import pytest


@pytest.mark.parametrize("filename,expected", [
    ('default', {'default': 'base-requirements.in'}),
    ('dev', {'default': 'requirements.in', 'dev': 'dev-requirements.in'})
])
def test_get_config(filename, expected):
    from snakepit.config import get_config
    config = get_config('tests/fixtures/yaml/{}.yml'.format(filename))
    assert config == expected


def test_error_if_config_does_not_exist():
    from snakepit.config import get_config
    from snakepit.exceptions import ConfigDoesNotExist

    with pytest.raises(ConfigDoesNotExist):
        get_config('not_found.yml')


def test_error_if_invalid_config():
    from snakepit.config import get_config
    from snakepit.exceptions import InvalidConfiguration

    with pytest.raises(InvalidConfiguration):
        get_config('tests/fixtures/yaml/invalid.yml')