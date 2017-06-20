from datetime import timedelta

import click

from thelocals import settings
from thelocals.services.search import search_by_interval
from thelocals.utils.command import command, YAML_TYPE


@click.group()
def cli():
    pass


@cli.command()
@click.argument('config', type=YAML_TYPE, default='config.yml')
@click.option('--interval', type=int, help='Интервал проверки новых объявлений в минутах', default=10)
@command
async def start(config, interval):

    for key, value in config.items():
        setattr(settings, key.upper(), value)

    await search_by_interval(timedelta(minutes=interval))
