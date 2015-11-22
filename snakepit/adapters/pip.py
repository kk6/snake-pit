# -*- coding: utf-8 -*-
"""Adapter of pip module."""

from __future__ import absolute_import, division, print_function, unicode_literals

import pip


def install(packages):
    """Execute `pip install`.

    :param packages: Package name list.
    :return: If `pip install` is successful, then return 0 else 1.

    """
    return pip.main(["install"] + [pkg for pkg in packages])


def uninstall(packages):
    """Execute `pip uninstall`.

    :param packages: Package name list.
    :return: If `pip install` is successful, then return 0 else 1.

    """
    return pip.main(["uninstall"] + ['-y'] + [pkg for pkg in packages])
