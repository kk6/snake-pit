# -*- coding: utf-8 -*-
"""
The main entry point.

Invoke as `snakepit' or `python -m snakepit'.
"""
import sys
from .cli import cli


if __name__ == '__main__':
    sys.exit(cli())
