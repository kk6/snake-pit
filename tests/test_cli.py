# -*- coding: utf-8 -*-
from click.testing import CliRunner


def test_version():
    from pit.cli import cli
    from pit import __version__
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert "snake-pit version: {}".format(__version__) in result.output


def test_install():
    from pit.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ['i'])
    assert "You must give at least one requirement to install" in result.output


def test_uninstall():
    from pit.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ['u'])
    assert "Do you want to continue?" in result.output
