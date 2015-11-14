# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import pip
import click

from . import echoes
from .groups import AliasedGroup
from .utils import classify_installed_or_not, re_edit_requirements


@click.group(cls=AliasedGroup)
def cli():
    """Depending on management packages, and then edit the requirements file.
    """


@cli.command()
@click.argument('packages', nargs=-1)
@click.option('--requirement', '-r', default='requirements.in',
              type=click.File('a'),
              help="Append package names to the given requirement file.")
def install(packages, requirement):
    """Install packages and write requirements file.

    To append package names were installed in requirements file,
    if the 'pip install' was successful.

    :param packages: Install packages.
    :param requirement: Output destination of package names.
    """
    if not packages:
        echoes.warn("You must give at least one requirement to install"
                    "(see 'pir --help')")
        return

    will_install, need_upgrade = classify_installed_or_not(packages)

    if need_upgrade:
        echoes.info(
            "Following packages installed. "
            "(use pip install --upgrade to upgrade): {}".format(", ".join(need_upgrade)))

    if not will_install:
        echoes.warn("There is no installable packages a new.")
        return

    raised = pip.main(["install"] + [pkg for pkg in will_install])
    if raised:
        return

    requirement.write('\n'.join(packages) + '\n')
    msg = "Append the following packages in {requirement}: {packages}"
    echoes.info(msg.format(requirement=requirement.name,
                           packages=", ".join(will_install)))


@cli.command()
@click.argument('packages', nargs=-1)
@click.option('--requirement', '-r', default='requirements.in',
              type=click.File('r'),
              help="Remove package names from the given requirement file.")
@click.confirmation_option(help="Are you sure you want to uninstall these packages?")
def uninstall(packages, requirement):
    """Uninstall packages and remove from requirements file.

    To Remove uninstalled packages from requirements file,
    if the 'pip uninstall' was successful.

    :param packages: Uninstall packages.
    :param requirement: Output destination of left package names.
    """
    msg = (
        "You must give at least one requirement to uninstall"
        "(see 'pir --help')"
    )
    if not packages:
        echoes.err(msg)
        return

    uninstalled_packages = []
    for pkg in packages:
        if pkg in uninstalled_packages:
            # Already installed
            continue
        if pip.main(["uninstall"] + ['-y'] + [pkg]):
            # Uninstall failed.
            continue
        else:
            uninstalled_packages.append(pkg)

    content = re_edit_requirements(requirement.readlines(), packages)
    with open(requirement.name, 'w') as f:
        f.write(content)
    msg = "Remove the following packages from {requirement}: {packages}"
    echoes.info(msg.format(requirement=requirement.name,
                           packages=", ".join(uninstalled_packages)))
