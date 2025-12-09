"""Tile drawing module - delegates to theme system."""
from pathlib import Path
from typing import List, Union

from aoc_tiles.config import Config
from aoc_tiles.leaderboard import DayScores
from aoc_tiles.themes import get_theme, Theme


class TileDrawer:
    """Draws tiles using the configured theme."""

    def __init__(self, config: Config):
        self.config = config
        self.theme: Theme = get_theme(config)

    def draw_tile(
            self, day: str, languages: List[str], day_scores: Union[DayScores, None], path: Path, stars: int
    ):
        """Saves a graphic for a given day and year. Returns the path to it."""
        self.theme.draw_tile(day, languages, day_scores, path, stars)
