import argparse
import dataclasses
from dataclasses import fields
from pathlib import Path
from typing import Literal

import rich.traceback

from aoc_tiles.config import Config
from aoc_tiles.make_tiles import TileMaker


def type_for_field(f):
    if isinstance(f.type, type(Path)):
        return Path
    elif f.default is not None and isinstance(f.default, list):
        return lambda x: x.split(',')  # Split comma-separated strings into lists
    elif f.type == bool:
        def bool_parser(value):
            if value.lower() in {'true', '1', 'yes', 'y'}:
                return True
            elif value.lower() in {'false', '0', 'no', 'n'}:
                return False
            else:
                raise argparse.ArgumentTypeError(f'Invalid value for boolean: {value}')

        return bool_parser
    return f.type


def cli_parser(datacls):
    parser = argparse.ArgumentParser(description='CLI for Config dataclass')
    for field in fields(datacls):
        if field.init:
            if_possible_values = ""
            if getattr(field.type, "__origin__", None) is Literal:
                if_possible_values = f"\nPossible values: [{','.join(field.type.__args__)}]"
            if_default = f'\nDefault: "{field.default}"' if field.default != dataclasses.MISSING else ""
            kwargs = {
                'type': type_for_field(field),
                'default': field.default,
                'help': field.metadata.get('help', field.name) + if_possible_values + if_default,
            }
            if field.type == bool:
                del kwargs['type']
                kwargs['action'] = 'store_true'
            # print(kwargs)
            parser.add_argument(f'--{field.name.replace("_", "-")}', **kwargs)
    return parser.parse_args()


def main():
    rich.traceback.install()
    args = cli_parser(Config)
    print(args)
    exit()
    config = Config()
    TileMaker(config).make_tiles()


if __name__ == "__main__":
    main()
