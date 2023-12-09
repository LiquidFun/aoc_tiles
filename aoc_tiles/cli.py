import argparse
import dataclasses
import functools
from dataclasses import fields
from pathlib import Path
from typing import Literal, Union, get_args, List, get_origin

import rich.traceback

from aoc_tiles.config import Config
from aoc_tiles.make_tiles import TileMaker


def literal_or_error(value, literal_type: type):
    type_literals = get_args(literal_type)
    if value not in type_literals:
        raise argparse.ArgumentTypeError(f"Expected {literal_type}, but received '{value}'")
    return value


def type_for_field(field):
    if "type" in field.metadata:
        return field.metadata["type"]
    elif getattr(field.type, "__origin__", None) is Literal:
        return functools.partial(literal_or_error, literal_type=field.type)
    elif getattr(field.type, "__origin__", None) is Path:
        return Path
    elif get_origin(field.type) == list or get_origin(field.type) == List:
        return lambda x: x.split(",")
    elif field.type == bool:

        def bool_parser(value):
            if value.lower() in {"true", "1", "yes", "y"}:
                return True
            elif value.lower() in {"false", "0", "no", "n"}:
                return False
            else:
                raise argparse.ArgumentTypeError(f"Invalid value for boolean: {value}")

        return bool_parser
    return field.type


def cli_parse_config(datacls):
    parser = argparse.ArgumentParser(description="CLI for Config dataclass")
    for field in fields(datacls):
        if field.init:
            if_possible_values = ""
            if getattr(field.type, "__origin__", None) is Literal:
                if_possible_values = f"\nPossible values: [{','.join(field.type.__args__)}]"
            if_default = f'\nDefault: "{field.default}"' if field.default != dataclasses.MISSING else ""
            kwargs = {
                "type": type_for_field(field),
                "help": field.metadata.get("help", field.name) + if_possible_values + if_default,
            }

            if hasattr(field, "default") and field.default != dataclasses.MISSING:
                kwargs["default"] = field.default
            elif hasattr(field, "default_factory") and field.default_factory != dataclasses.MISSING:
                kwargs["default"] = field.default_factory()

            if "default" in kwargs and isinstance(kwargs["default"], list):
                kwargs["action"] = "store"

            if field.type == bool:
                del kwargs["type"]
                kwargs["action"] = "store_true"
            # print(kwargs)
            parser.add_argument(f'--{field.name.replace("_", "-")}', **kwargs)

    parser.add_argument(
        "positional args are ignored",
        nargs="*",
        help="Any non-keyword arguments are ignored. This is because pre-commit passes all arguments to the hook,"
             " and we don't want to fail the hook because of that.",
    )

    args = vars(parser.parse_args())
    del args["positional args are ignored"]
    return datacls(**args)


def main():
    rich.traceback.install()
    config = cli_parse_config(Config)
    TileMaker(config).make_tiles()


if __name__ == "__main__":
    main()
