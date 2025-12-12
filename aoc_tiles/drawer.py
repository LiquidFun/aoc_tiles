"""Tile drawing module - delegates to theme and animation systems."""

from pathlib import Path
from typing import List, Union

from PIL import Image

from aoc_tiles.animations import get_animation
from aoc_tiles.config import Config
from aoc_tiles.leaderboard import DayScores
from aoc_tiles.themes import get_theme, Theme


class TileDrawer:
    """Draws tiles using the configured theme and optional animation."""

    def __init__(self, config: Config):
        self.config = config
        self.theme: Theme = get_theme(config)
        self.animation = get_animation(config)

    def draw_tile(
        self,
        day: str,
        languages: List[str],
        day_scores: Union[DayScores, None],
        path: Path,
        stars: int,
    ):
        """Saves a graphic for a given day and year. Returns the path to it."""
        if self.animation:
            # For animations, we need the base image first
            # Create a temporary path for the base image
            temp_path = path.with_suffix(".tmp.png")
            self.theme.draw_tile(day, languages, day_scores, temp_path, stars)

            # Load the base image and create animation
            base_image = Image.open(temp_path)
            self.animation.animate(base_image, path)

            # Clean up temp file
            temp_path.unlink()
        else:
            self.theme.draw_tile(day, languages, day_scores, path, stars)
