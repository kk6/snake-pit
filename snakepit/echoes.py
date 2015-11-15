# -*- coding: utf-8 -*-
"""Wrapped functions for click.echo ."""
from __future__ import absolute_import, division, print_function, unicode_literals

import click


def info(message):
    """Display Information message.

    :param message: Information message

    """
    click.echo(message)


def success(message):
    """Display Success message.

    :param message: Success message

    """
    click.echo(click.style(message, fg='green'))


def warn(message):
    """Display Warning message.

    :param message: Warning message

    """
    click.echo(click.style(message, fg='yellow'))


def err(message):
    """Display Error message.

    :param message: Error message

    """
    click.echo(click.style(message, fg='red'))
