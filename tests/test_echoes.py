# -*- coding: utf-8 -*-
import click
from click.testing import CliRunner

from snakepit import echoes


def test_echo_info():
    @click.command()
    def test():
        echoes.info('info')

    runner = CliRunner()
    result = runner.invoke(test)
    assert not result.exception
    assert result.output == 'info\n'


def test_echo_success():
    @click.command()
    def test():
        echoes.success('success')

    runner = CliRunner()
    result = runner.invoke(test)
    assert not result.exception
    assert result.output == 'success\n'
    
    
def test_echo_warn():
    @click.command()
    def test():
        echoes.warn('warn')

    runner = CliRunner()
    result = runner.invoke(test)
    assert not result.exception
    assert result.output == 'warn\n'
    
    
def test_echo_err():
    @click.command()
    def test():
        echoes.err('err')

    runner = CliRunner()
    result = runner.invoke(test)
    assert not result.exception
    assert result.output == 'err\n'

