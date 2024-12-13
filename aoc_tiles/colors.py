# Location of yaml file where file extensions are mapped to colors
from functools import lru_cache
from pathlib import Path
from typing import Tuple, Dict

import yaml
from loguru import logger

GITHUB_LANGUAGES_PATH = Path(__file__).parent / "resources" / "github_languages.yaml"

# Until someone complains, I'll exclude languages which conflict with my language extensions
excludes = ["GCC Machine Description", "Standard ML"]
overrides = {"Jupyter Notebook": {"type": "programming"}}


@lru_cache
def github_languages_config() -> Dict[str, Dict]:
    with open(GITHUB_LANGUAGES_PATH) as file:
        logger.debug("Loading github_languages.yaml from {}", GITHUB_LANGUAGES_PATH)
        yaml_loader = yaml.CLoader if yaml.__with_libyaml__ else yaml.Loader
        if not yaml.__with_libyaml__:
            logger.warning("Using slow yaml parser (0.5s vs 0.1s)!")
        github_languages = yaml.load(file, Loader=yaml_loader)
        logger.debug("Loaded github_languages.yaml from {}", GITHUB_LANGUAGES_PATH)

        for language, override_dict in overrides.items():
            if language not in github_languages:
                github_languages[language] = {}
            github_languages[language].update(override_dict)

        return github_languages


@lru_cache
def extension_to_colors() -> Dict[str, str]:
    extension_to_color = {}
    for language, data in github_languages_config().items():
        if "color" in data and "extensions" in data and data["type"] == "programming" and language not in excludes:
            for extension in data["extensions"]:
                extension_to_color[extension.lower()] = data["color"]

    return extension_to_color


@lru_cache
def extension_to_programming_language() -> Dict[str, str]:
    extension_to_language = {}
    for language, data in github_languages_config().items():
        if "extensions" in data and data["type"] == "programming" and language not in excludes:
            for extension in data["extensions"]:
                extension_to_language[extension.lower()] = language

    return extension_to_language


def darker_color(c: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    return c[0] - 10, c[1] - 10, c[2] - 10, 255


# Luminance of color
def luminance(color):
    return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]


# How similar is color_a to color_b
def color_similarity(color_a, color_b, threshold):
    return abs(luminance(color_a) - luminance(color_b)) < threshold
