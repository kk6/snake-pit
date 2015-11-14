# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import re

import pip


def get_installed_package_set():
    return {p.key for p in pip.get_installed_distributions()}


def classify_installed_or_not(packages):
    installed = get_installed_package_set()
    will_install = set(packages) - installed
    need_upgrade = set(packages) & installed
    return will_install, need_upgrade


def re_edit_requirements(lines, will_remove):
    """
    Re-Edit requirements file

    :param lines: requirement.readlines()'s return value.
    :param will_remove: Will be removed packages.
    :return: The contents of the file after re-editing.
    """
    pattern = re.compile('^[\w0-9\-.]+')
    re_editing = []
    for line in lines:
        matched = pattern.match(line)
        if not matched or matched.group().lower() not in will_remove:
            re_editing.append(line)
    if re_editing[-1] != '\n':
        re_editing.append('\n')
    return ''.join(re_editing)
