# Location of yaml file where file extensions are mapped to colors
from pathlib import Path
from typing import Tuple

import yaml

GITHUB_LANGUAGES_PATH = Path(__file__).parent / "resources" / "github_languages.yml"


def get_extension_to_colors():
    extension_to_color = {}
    with open(GITHUB_LANGUAGES_PATH) as file:
        github_languages = yaml.load(file, Loader=yaml.FullLoader)
        for language, data in github_languages.items():
            if "color" in data and "extensions" in data and data["type"] == "programming":
                for extension in data["extensions"]:
                    extension_to_color[extension.lower()] = data["color"]
    return extension_to_color


def darker_color(c: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    return c[0] - 10, c[1] - 10, c[2] - 10, 255


# Luminance of color
def luminance(color):
    return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]


# How similar is color_a to color_b
def color_similarity(color_a, color_b, threshold):
    return abs(luminance(color_a) - luminance(color_b)) < threshold
