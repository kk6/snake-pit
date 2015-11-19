# -*- coding: utf-8 -*-
import pytest


@pytest.mark.parametrize("packages,expected", [
    (['pkg1', 'pkg2', 'pkg3'], ({'pkg1', 'pkg3'}, {'pkg2'})),
])
def test_classify_installed_or_not(monkeypatch, packages, expected):
    def mockreturn():
        return {'pkg2'}
    from snakepit import dists
    monkeypatch.setattr(dists, 'get_installed_package_set', mockreturn)
    from snakepit.dists import classify_installed_or_not

    rv = classify_installed_or_not(packages)
    assert rv == expected
