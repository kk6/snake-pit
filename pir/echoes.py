# -*- coding: utf-8 -*-

import click


def info(message):
    """Display Information message

    :param message: Information message

    """
    click.echo(message)


def warn(message):
    """Display Warning message

    :param message: Warning message

    """
    click.echo(click.style(message, fg='yellow'))


def err(message):
    """Display Error message

    :param message: Error message

    """
    click.echo(click.style(message, fg='red'))