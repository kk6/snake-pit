# -*- coding: utf-8 -*-

"""Utilities."""

from __future__ import absolute_import, division, print_function, unicode_literals

import re


def re_edit(lines, will_remove):
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
    return ''.join(re_editing)
