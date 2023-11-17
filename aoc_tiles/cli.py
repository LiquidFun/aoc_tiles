import rich.traceback

from aoc_tiles.config import Config
from aoc_tiles.tiles import AoCTiles


def main():
    rich.traceback.install()
    config = Config()
    AoCTiles(config).run()


if __name__ == "__main__":
    main()

