# -*- coding: utf-8 -*-
import pytest


@pytest.fixture('module')
def finder():
    from snakepit.dists import DistFinder
    return DistFinder()


def test_choose_installed(finder):
    packages = ['click', 'pytest', 'nose', 'django']

    installed = finder.choose_installed(packages)
    assert installed == {'click', 'pytest'}


def test_choose_not_installed(finder):
    packages = ['click', 'pytest', 'nose', 'django']

    not_instslled = finder.choose_not_installed(packages)
    assert not_instslled == {'nose', 'django'}


def test_get_distribution(finder):
    dist = finder.get_distribution('pytest')
    assert dist.name == 'pytest'


def test_get_dependencies(finder):
    deps = finder.get_dependencies('pytest')
    assert {d.name for d in deps} == {'pytest', 'py'}


def test_get_dependencies_with_side_effect(finder):
    from snakepit.exceptions import DistributionNotFound
    with pytest.raises(DistributionNotFound):
        finder.get_dependencies('flask')
