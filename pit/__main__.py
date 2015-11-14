# -*- coding: utf-8 -*-
"""
The main entry point.

Invoke as `pit' or `python -m pit'.
"""
import sys
from .cli import cli


if __name__ == '__main__':
    sys.exit(cli())
