# -*- coding: utf-8 -*-
from click.testing import CliRunner


def test_version():
    from snakepit.cli import cli
    from snakepit import __version__
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert "snake-pit, version {}".format(__version__) in result.output


def test_install():
    from snakepit.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ['i'])
    assert result.exit_code == 0
    assert "You must give at least one requirement to install" in result.output

    result = runner.invoke(cli, ['i', 'XXX'])
    assert result.exit_code == 1
    assert "No matching distribution found for XXX" in result.output

    result = runner.invoke(cli, ['i', 'pytest'])
    assert result.exit_code == 0
    assert "Following packages installed." in result.output
    assert "There is no installable packages a new." in result.output

    result = runner.invoke(cli, ['i', 'XXX', '-n', 'YYY'])
    assert result.exit_code == 1


def test_uninstall():
    from snakepit.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ['u'], 'y')
    assert result.exit_code == 1
    assert "You must give at least one requirement to uninstall" in result.output

    result = runner.invoke(cli, ['u', 'XXX'], 'y')
    assert result.exit_code == 1
    assert "XXX is not installed" in result.output

    result = runner.invoke(cli, ['u', 'XXX', '-n', 'YYY'], 'y')
    assert result.exit_code == 1
