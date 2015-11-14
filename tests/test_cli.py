# -*- coding: utf-8 -*-
import pytest
from click.testing import CliRunner


def test_install():
    from pir.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ['i'])
    assert "You must give at least one requirement to install" in result.output


def test_uninstall():
    from pir.cli import cli
    runner = CliRunner()
    result = runner.invoke(cli, ['u'])
    assert "Do you want to continue?" in result.output
