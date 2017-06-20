import asyncio
from functools import wraps

import yaml
import click

from thelocals import setup, teardown


def command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        setup()
        try:
            asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
        finally:
            teardown()
    return wrapper


class YAMLType(click.File):

    def convert(self, value, param, ctx):
        result = super().convert(value, param, ctx)
        try:
            return yaml.load(result)
        except yaml.scanner.ScannerError:
            self.fail('File is not a valid YAML file.', param, ctx)


YAML_TYPE = YAMLType()
