# -*- coding: utf-8 -*-
"""Main `pit` CLI."""
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from textwrap import dedent

import click

import pip

from . import __version__
from . import echoes
from .config import DEFAULT_CONFIG, get_config, get_requirements_path
from .exceptions import ConfigDoesNotExist, InvalidConfiguration
from .groups import AliasedGroup
from .utils import (
    classify_installed_or_not,
    get_dependencies,
    get_installed_package_set,
    re_edit_requirements,
)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(cls=AliasedGroup, context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, '--version', '-V', prog_name='snake-pit')
@click.pass_context
def cli(ctx):
    """Depending on management packages, and then edit the requirements file.
    """
    ctx.obj = {}
    try:
        ctx.obj['CONFIG'] = get_config()
    except (ConfigDoesNotExist, InvalidConfiguration) as e:
        echoes.err(str(e))
        echoes.warn("Now use default config.")
        ctx.obj['CONFIG'] = DEFAULT_CONFIG


@cli.command()
@click.argument('packages', nargs=-1)
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

    if not packages:
        echoes.warn("You must give at least one requirement to install"
                    "(see 'snakepit --help')")
        sys.exit(0)

    if not requirement:
        try:
            requirement = get_requirements_path(ctx.obj['CONFIG'], name)
        except InvalidConfiguration as e:
            echoes.err(str(e))
            sys.exit(1)

    requirements_file = click.open_file(requirement, 'a')

    will_install, need_upgrade = classify_installed_or_not(packages)

    if need_upgrade:
        echoes.info(
            "Following packages installed. "
            "(use pip install --upgrade to upgrade): {}".format(", ".join(need_upgrade)))

    if not will_install:
        echoes.warn("There is no installable packages a new.")
        sys.exit(0)

    raised = pip.main(["install"] + [pkg for pkg in will_install])
    if raised:
        sys.exit(1)

    requirements_file.write('\n'.join(packages) + '\n')
    msg = "Append the following packages in {requirement}: {packages}"
    echoes.info(msg.format(requirement=requirements_file.name,
                           packages=", ".join(will_install)))
    if quiet:
        sys.exit(0)
    requirements_file.seek(0)
    with open(requirements_file.name, 'r') as f:
        echoes.info("{} has been updated as follows:".format(requirements_file.name))
        echoes.success(f.read())


@cli.command()
@click.argument('packages', nargs=-1)
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
    if not packages:
        echoes.err(
            "You must give at least one requirement to uninstall"
            "(see 'snakepit --help')"
        )
        sys.exit(1)

    if not requirement:
        try:
            requirement = get_requirements_path(ctx.obj['CONFIG'], name)
        except InvalidConfiguration as e:
            echoes.err(str(e))
            sys.exit(1)

    requirements_file = click.open_file(requirement, 'r')

    uninstalled_packages = []
    for pkg in packages:
        if pkg in uninstalled_packages:
            # Already installed
            continue
        if pkg not in get_installed_package_set():
            echoes.err("{} is not installed".format(pkg))
            continue
        if pip.main(["uninstall"] + ['-y'] + get_dependencies(pkg)):
            # Uninstall failed.
            continue
        else:
            uninstalled_packages.append(pkg)

    if not uninstalled_packages:
        sys.exit(1)

    content = re_edit_requirements(requirements_file.readlines(), packages)
    with open(requirements_file.name, 'w') as f:
        f.write(content)
    msg = "Remove the following packages from {requirement}: {packages}"
    echoes.info(msg.format(requirement=requirements_file.name,
                           packages=", ".join(uninstalled_packages)))
    if quiet:
        sys.exit(0)

    with open(requirements_file.name, 'r') as f:
        echoes.info("{} has been updated as follows:".format(requirements_file.name))
        echoes.success(f.read())
