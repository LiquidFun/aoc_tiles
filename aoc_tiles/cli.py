import rich.traceback

from aoc_tiles.config import Config
from aoc_tiles.make_tiles import TileMaker


def main():
    rich.traceback.install()
    config = Config()
    TileMaker(config).make_tiles()


if __name__ == "__main__":
    main()

