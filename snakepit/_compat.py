# -*- coding: utf-8 -*-
"""
Python 2 and Python 3 compatibility.

"""
import sys

PY2 = sys.version_info[0] == 2


if PY2:
    FileNotFoundError = IOError
else:
    FileNotFoundError = FileNotFoundError
