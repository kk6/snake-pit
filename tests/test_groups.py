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
    from pir.groups import AliasedGroup

    @click.group(cls=AliasedGroup)
    def pir():
        click.echo("I'm pir")

    @pir.command()
    def install():
        click.echo("I'm install")

    @pir.command()
    def uninstall():
        click.echo("I'm uninstall")

    @pir.command()
    def update():
        click.echo("I'm update")

    runner = CliRunner()
    result = runner.invoke(pir, [cmd])
    assert expected_output in result.output
