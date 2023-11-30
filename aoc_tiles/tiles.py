from pathlib import Path
import re
import json
from typing import Literal, Union, List, Dict, Tuple, Optional


from aoc_tiles.drawer import TileDrawer
from aoc_tiles.leaderboard import DayScores, request_leaderboard

from aoc_tiles.colors import extension_to_colors
from aoc_tiles.config import Config
from aoc_tiles.html import HTML

README_TILES_BEGIN = "<!-- AOC TILES BEGIN -->"
README_TILES_END = "<!-- AOC TILES END -->"


class AoCTiles:
    def __init__(self, config: Config):
        self.config = config
        self.tile_drawer = TileDrawer(self.config)

    def handle_day(
        self, day: int, year: int, solutions: List[str], html: HTML, day_scores: Optional[DayScores], needs_update: bool
    ):
        languages = []
        for solution in solutions:
            extension = "." + solution.split(".")[-1]
            if extension in extension_to_colors() and extension not in languages:
                languages.append(extension)
        solution_link = solutions[0] if solutions else None
        if self.config.debug:
            if day == 25:
                languages = []
        day_graphic_path = self.config.image_dir / f"{year:04}/{day:02}.png"
        day_graphic_path.parent.mkdir(parents=True, exist_ok=True)
        if not day_graphic_path.exists() or needs_update:
            self.tile_drawer.draw_tile(f"{day:02}", languages, day_scores, day_graphic_path)
        day_graphic_path = day_graphic_path.relative_to(self.config.aoc_dir)
        with html.tag("a", href=str(solution_link)):
            html.tag("img", closing=False, src=day_graphic_path.as_posix(), width=self.config.tile_width_px)

    def fill_empty_days_in_dict(self, day_to_solutions: Dict[int, List[str]], max_day) -> None:
        if not self.config.create_all_days and len(day_to_solutions) == 0:
            print(f"Current year has no solutions!")
        for day in range(1, max_day + 1):
            if day not in day_to_solutions:
                day_to_solutions[day] = []

    def handle_year(self, year: int, day_to_solutions: Dict[int, List[str]]):
        leaderboard = request_leaderboard(year, self.config)
        if self.config.debug:
            leaderboard[25] = None
            leaderboard[24] = DayScores("22:22:22", "12313", "0")
            day_to_solutions[23] = []
        html = HTML()
        with html.tag("h1", align="center"):
            stars = sum(
                (ds.time1 is not None) + (ds.time2 is not None) for ds in leaderboard.values() if ds is not None
            )
            html.push(f"{year} - {stars} ⭐")
        max_day = 25 if self.config.create_all_days else max(*day_to_solutions, *leaderboard)
        self.fill_empty_days_in_dict(day_to_solutions, max_day)

        completed_solutions = dict()
        completed_cache_path = self.config.cache_dir / f"completed-{year}.json"
        if completed_cache_path.exists():
            with open(completed_cache_path, "r") as file:
                completed_solutions = {int(day): solutions for day, solutions in json.load(file).items()}

        for day, solutions in sorted(day_to_solutions.items()):
            self.handle_day(day, year, solutions, html, leaderboard.get(day), completed_solutions.get(day) != solutions)

        with open(completed_cache_path, "w") as file:
            completed_days = [day for day, scores in leaderboard.items() if scores.time2 is not None]
            file.write(
                json.dumps({day: solutions for day, solutions in day_to_solutions.items() if day in completed_days})
            )

        with open(self.config.readme_path, "r", encoding="utf-8") as file:
            text = file.read()
            begin = README_TILES_BEGIN
            end = README_TILES_END
            assert begin in text and end in text, (
                f"Could not find AOC TILES markers '{begin}' and '{end}' in the "
                f"README.md! Make sure to add them to the README at {self.config.readme_path}."
            )
            pattern = re.compile(rf"{begin}.*{end}", re.DOTALL | re.MULTILINE)
            new_text = pattern.sub(f"{begin}\n{html}\n{end}", text)

        with open(self.config.readme_path, "w", encoding="utf-8") as file:
            file.write(str(new_text))

    def run(self):
        print("Running AoC-Tiles")
        for year, day_to_solutions_list in self.get_solution_paths_dict_for_years().items():
            print(f"=== Generating table for year {year} ===")
            print(year, day_to_solutions_list)
            self.handle_year(year, day_to_solutions_list)
