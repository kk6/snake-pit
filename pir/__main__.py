# -*- coding: utf-8 -*-
"""
The main entry point.

Invoke as `pir' or `python -m pir'.
"""
import sys
from .cli import cli


if __name__ == '__main__':
    sys.exit(cli())
