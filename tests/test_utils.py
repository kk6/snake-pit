# -*- coding: utf-8 -*-
"""
snakepit.utils
--------------

Utilities.
"""
from textwrap import dedent


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
