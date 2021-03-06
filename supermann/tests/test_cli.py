from __future__ import absolute_import, unicode_literals

import os.path

import click.testing
import mock

import supermann.cli


def main(args=[], env=None, command=supermann.cli.main):
    runner = click.testing.CliRunner()
    result = runner.invoke(command, args, env=env)
    print result.output
    assert result.exit_code == 0
    return result


@mock.patch('supermann.core.Supermann')
class TestCLI(object):
    def test_main_with_all(self, supermann_cls):
        main(['--log-level', 'INFO', 'localhost', '5555'])
        supermann_cls.assert_called_with('localhost', 5555)

    def test_main_with_args(self, supermann_cls):
        main(['example.com', '6666'])
        supermann_cls.assert_called_with('example.com', 6666)

    def test_main_with_some_args(self, supermann_cls):
        main(['example.com'])
        supermann_cls.assert_called_with('example.com', 5555)

    def test_main_without_args(self, supermann_cls):
        main()
        supermann_cls.assert_called_with('localhost', 5555)

    def test_main_with_env(self, supermann_cls):
        main(env={
            'RIEMANN_HOST': 'example.com',
            'RIEMANN_PORT': '6666'
        })
        supermann_cls.assert_called_with('example.com', 6666)

    @mock.patch('supermann.utils.configure_logging')
    def test_log_level(self, configure_logging, supermann_cls):
        main(['--log-level', 'WARNING'])
        configure_logging.assert_called_with('WARNING')

    @mock.patch('supermann.utils.configure_logging')
    def test_from_file(self, configure_logging, supermann_cls):
        path = os.path.join(os.path.dirname(__file__), 'supermann.args')
        main([path], command=supermann.cli.from_file)
        configure_logging.assert_called_with('DEBUG')
        supermann_cls.assert_called_with('example.com', 6666)
