from functools import lru_cache
from pathlib import Path

from PIL import ImageFont

FONTS_PATH = Path(__file__).parent / "resources" / "fonts"


@lru_cache
def get_font(size: int, path: Path):
    return ImageFont.truetype(str(path), size)


# Note that the fonts sizes are specifically adjusted to the following fonts, if you change the fonts
# you might need to adjust the font sizes and text locations in the rest of the script.


def main_font(size: int) -> ImageFont:
    return get_font(size, FONTS_PATH / "PaytoneOne.ttf")


def secondary_font(size: int) -> ImageFont:
    return get_font(size, FONTS_PATH / "SourceCodePro-Regular.otf")
