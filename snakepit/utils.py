# -*- coding: utf-8 -*-

"""Utilities."""

from __future__ import absolute_import, division, print_function, unicode_literals

import re

import pip

from pkg_resources import working_set


def get_installed_package_set():
    """Return installed packages.

    :return: Installed packages.
    :rtype: set

    """
    return {p.key for p in pip.get_installed_distributions()}


def classify_installed_or_not(packages):
    """Classify packages installed or not.

    :param packages: Passed packages by user.
    :return: Install candidates and installed packages.
    :rtype: tuple

    """
    installed = get_installed_package_set()
    will_install = set(packages) - installed
    need_upgrade = set(packages) & installed
    return will_install, need_upgrade


def re_edit_requirements(lines, will_remove):
    """Re-Edit requirements file.

    :param lines: requirement.readlines()'s return value.
    :param will_remove: Will be removed packages.
    :return: The contents of the file after re-editing.
    :rtype: str

    """
    pattern = re.compile('^[\w0-9\-.]+')
    re_editing = []
    for line in lines:
        matched = pattern.match(line)
        if not matched or matched.group().lower() not in will_remove:
            re_editing.append(line)
    if re_editing and re_editing[-1] != '\n':
        re_editing.append('\n')
    return ''.join(re_editing)


def get_dependency_tree(package):
    """Return dependency tree by nested list.

    :param package: Top level package.
    :return: Dependency tree.
    :rtype: list

    """
    tree = [package]
    top_pkg = working_set.by_key[package]
    for p in top_pkg.requires():
        tree.append(get_dependency_tree(p.key))
    return tree


def get_dependencies(package):
    """Return dependencies by flat list.

    :param package: Top level package.
    :return: Dependencies
    :rtype: list

    """
    dependencies = [package]
    top_pkg = working_set.by_key[package]
    for p in top_pkg.requires():
        dependencies.extend(get_dependencies(p.key))
    return dependencies
