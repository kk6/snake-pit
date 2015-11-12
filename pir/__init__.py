# -*- coding: utf-8 -*-
import pip
import click

__version__ = '0.1.0'


@click.command()
@click.argument('packages', nargs=-1)
@click.option('--requirement', '-r', default='requirements.in',
              type=click.File('a'),
              help="Append package names to the given requirement file.")
def main(packages, requirement):
    """
    Main

    To append package names were installed in requirements file,
    if the 'pip install' was successful.

    :param packages: Install packages.
    :param requirement: Output destination of package names.
    """
    msg = (
        "You must give at least one requirement to install"
        "(see 'pir --help')"
    )
    if not packages:
        click.echo(click.style(msg, fg='yellow'))
        return

    raised = pip.main(["install"] + [pkg for pkg in packages])
    if raised:
        return

    requirement.write('\n'.join(packages) + '\n')
    msg = "Append the following packages in {requirement}: {packages}"
    click.echo(msg.format(requirement=requirement.name,
                          packages=", ".join(packages)))


if __name__ == '__main__':
    main()

