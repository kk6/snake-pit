# -*- coding: utf-8 -*-
import re

import pip
import click

__version__ = '0.1.2'


class AliasedGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: {}'.format(', '.join(sorted(matches))))


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
        click.echo(click.style(msg, fg='red'))
        return

    raised = pip.main(["uninstall"] + ['-y'] + [pkg for pkg in packages])
    if raised:
        return

    output = []
    pattern = re.compile('^[\w0-9\-.]+')
    for line in requirement.readlines():
        match_obj = pattern.match(line)
        if match_obj:
            matched_pkg = match_obj.group().lower()
            if matched_pkg not in packages:
                output.append(line)
        else:
            output.append(line)
    content = '\n'.join(output)
    if output[-1] != '\n':
        output += '\n'
    with open(requirement.name, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    cli()

