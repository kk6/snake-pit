# -*- coding: utf-8 -*-
import pytest


@pytest.mark.parametrize("cmd,expected_output", [
    ('install', "I'm install"),
    ('i', "I'm install"),
    ('uninstall', "I'm uninstall"),
    ('un', "I'm uninstall"),
    ('u', "Too many matches: uninstall, update"),
    ('XXX', 'No such command'),
])
def test_aliased_group(cmd, expected_output):
    import click
    from click.testing import CliRunner
    from snakepit.groups import AliasedGroup

    @click.group(cls=AliasedGroup)
    def pit():
        click.echo("I'm snakepit")

    @pit.command()
    def install():
        click.echo("I'm install")

    @pit.command()
    def uninstall():
        click.echo("I'm uninstall")

    @pit.command()
    def update():
        click.echo("I'm update")

    runner = CliRunner()
    result = runner.invoke(pit, [cmd])
    assert expected_output in result.output
