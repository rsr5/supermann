from __future__ import absolute_import, unicode_literals

import click

import supermann.core
import supermann.metrics
import supermann.metrics.system
import supermann.metrics.process
import supermann.signals
import supermann.utils


@click.command()
@click.version_option(version=supermann.__version__)
@click.option(
    '-l', '--log-level', default='INFO',
    type=click.Choice(supermann.utils.LOG_LEVELS.keys()),
    help="One of CRITICAL, ERROR, WARNING, INFO, DEBUG.")
@click.argument(
    'host', type=click.STRING, default='localhost', envvar='RIEMANN_HOST')
@click.argument(
    'port', type=click.INT, default=5555, envvar='RIEMANN_PORT')
def main(log_level, host, port):
    # Log messages are sent to stderr, and Supervisor takes care of the rest
    supermann.utils.configure_logging(log_level)

    # Supermann will attempt to run forever
    supermann.core.Supermann(host, port).with_all_recivers().run()


@click.command()
@click.argument('config', type=click.File('r'))
def from_file(config):
    main.main(args=config.read().split())
