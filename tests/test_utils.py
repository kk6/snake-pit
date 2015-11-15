# -*- coding: utf-8 -*-
"""
snakepit.utils
--------------

Utilities.
"""
from textwrap import dedent
import pytest


@pytest.mark.parametrize("packages,expected", [
    (['pkg1', 'pkg2', 'pkg3'], ({'pkg1', 'pkg3'}, {'pkg2'})),
])
def test_classify_installed_or_not(monkeypatch, packages, expected):
    def mockreturn():
        return {'pkg2'}
    from snakepit import utils
    monkeypatch.setattr(utils, 'get_installed_package_set', mockreturn)
    from snakepit.utils import classify_installed_or_not

    rv = classify_installed_or_not(packages)
    assert rv == expected


def test_re_edit_requirements():
    from snakepit.utils import re_edit_requirements
    before = [
        "# requirements.in\n",
        "flask\n",
        "pytest\n",
        "\n",
    ]
    after = dedent("""\
        # requirements.in
        pytest

    """)
    content = re_edit_requirements(before, ['flask'])
    assert content == after
