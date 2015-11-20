# -*- coding: utf-8 -*-
"""Main `pit` CLI."""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
from textwrap import dedent

import click

from . import __version__
from . import echoes
from .adapters import pip
from .config import DEFAULT_CONFIG, get_config, get_requirements_file
from .dists import DistFinder
from .exceptions import (
    ConfigDoesNotExist,
    InvalidConfiguration,
    RequirementsKeyError,
)
from .groups import AliasedGroup
from .utils import re_edit_requirements

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CONFIG_PATH = os.environ.get('PIT_CONFIG_PATH', 'pit.yml')


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, '--version', '-V', prog_name='snake-pit')
@click.pass_context
def cli(ctx):
    """Depending on management packages, and then edit the requirements file.
    """
    ctx.obj = {}
    try:
        ctx.obj['CONFIG'] = get_config(CONFIG_PATH)
    except (ConfigDoesNotExist, InvalidConfiguration) as e:
        echoes.err(str(e))
        echoes.warn("Instead, it uses the default configuration.")
        ctx.obj['CONFIG'] = DEFAULT_CONFIG


@cli.command()
@click.argument('packages', nargs=-1, required=True)
@click.option(
    '--requirement', '-r', type=click.Path(exists=True),
    help="Append package names to the given requirement file."
)
@click.option('--quiet', '-q', is_flag=True, help='Do not display the output result.')
@click.option('--name', '-n', help=dedent("""\
    Specify requirements file name.
    This option takes precedence over the '-r' option.
    """))
@click.pass_context
def install(ctx, packages, requirement, quiet, name):
    """Install packages and write requirements file.

    To append package names were installed in requirements file,
    if the 'pip install' was successful.

    """
    try:
        requirements_file = get_requirements_file(
            ctx.obj['CONFIG'], requirement, name, mode='a+'
        )
    except RequirementsKeyError as e:
        echoes.err(str(e))
        sys.exit(2)

    finder = DistFinder()

    upgradable_packages = finder.choose_installed(packages)
    if upgradable_packages:
        echoes.info(
            "Following packages installed. "
            "(use pip install --upgrade to upgrade): {}".format(
                ", ".join(upgradable_packages)
            )
        )

    installable_packages = finder.choose_not_installed(packages)
    if not installable_packages:
        echoes.warn("There is no installable packages a new.")
        sys.exit(0)

    raised = pip.install(installable_packages)
    if raised:
        sys.exit(2)

    requirements_file.write('\n'.join(packages) + '\n')
    echoes.info("Append the following packages in {requirement}: {packages}".format(
        requirement=requirements_file.name, packages=", ".join(installable_packages)
    ))

    if not quiet:
        requirements_file.seek(0)
        echoes.info("{} has been updated as follows:".format(requirements_file.name))
        echoes.success(requirements_file.read())
        requirements_file.close()


@cli.command()
@click.argument('packages', nargs=-1, required=True)
@click.option(
    '--requirement', '-r', type=click.Path(exists=True),
    help="Remove package names from the given requirement file."
)
@click.option('--quiet', '-q', is_flag=True, help='Do not display the output result.')
@click.option('--name', '-n', help=dedent("""\
    Specify requirements file name.
    This option takes precedence over the '-r' option.
    """))
@click.confirmation_option(help="Are you sure you want to uninstall these packages?")
@click.pass_context
def uninstall(ctx, packages, requirement, quiet, name):
    """Uninstall packages and remove from requirements file.

    To Remove uninstalled packages from requirements file,
    if the 'pip uninstall' was successful.

    """
    try:
        requirements_file = get_requirements_file(
            ctx.obj['CONFIG'], requirement, name, mode='r'
        )
    except RequirementsKeyError as e:
        echoes.err(str(e))
        sys.exit(2)

    finder = DistFinder()

    # Warning packages that are not installed.
    not_installed = finder.choose_not_installed(packages)
    if not_installed:
        echoes.err(
            "Following packages are not installed: {}".format(
                ", ".join(not_installed)
            )
        )

    # Run the installation.
    uninstalled_packages = []
    installed = finder.choose_installed(packages)
    for pkg in installed:
        dependencies = finder.get_dependencies(pkg)
        if pkg not in uninstalled_packages:
            if pip.uninstall(list({d.name for d in dependencies})):
                # Uninstall failed.
                continue
            else:
                uninstalled_packages.append(pkg)

    if not uninstalled_packages:
        sys.exit(2)

    content = re_edit_requirements(requirements_file.readlines(), packages)
    with open(requirements_file.name, 'w') as f:
        f.write(content)

    echoes.info("Remove the following packages from {requirement}: {packages}".format(
        requirement=requirements_file.name, packages=", ".join(uninstalled_packages)
    ))

    if not quiet:
        echoes.info("{} has been updated as follows:".format(requirements_file.name))
        echoes.success(content)
