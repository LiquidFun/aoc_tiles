import concurrent
import json
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Dict, Set, List, Optional

from aoc_tiles.colors import extension_to_colors
from aoc_tiles.config import Config
from aoc_tiles.drawer import TileDrawer
from aoc_tiles.html import HTML
from aoc_tiles.leaderboard import DayScores, request_leaderboard
from aoc_tiles.solutions import SolutionFinder


README_TILES_BEGIN = "<!-- AOC TILES BEGIN -->"
README_TILES_END = "<!-- AOC TILES END -->"


@dataclass
class YearData:
    day_to_scores: Dict[int, DayScores]
    day_to_paths: Dict[int, List[Path]]
    is_day_solved: Set[int]


@dataclass
class SolveData:
    year_to_data: Dict[int, YearData]


class TileMaker:
    def __init__(self, config: Config):
        self.config = config
        self.tile_drawer = TileDrawer(config)

    def _is_solved(self, solved, solution):
        is_solved_func = {
            "on_leaderboard": lambda a, b: bool(a),
            "file_exists": lambda a, b: bool(b),
            "either": lambda a, b: bool(a or b),
            "both": lambda a, b: bool(a and b),
        }[self.config.count_as_solved_when]

        return is_solved_func(solved, solution)

    def compose_solve_data(self) -> SolveData:
        is_solution_paths_needed = self.config.what_to_show_on_right_side in [
            "loc"
        ] or self.config.count_as_solved_when in ["file_exists", "both", "either"]
        solution_paths_by_year = {}
        years = []
        if is_solution_paths_needed:
            solution_finder = SolutionFinder(self.config)
            solution_paths_by_year = solution_finder.get_solution_paths_by_year(self.config.aoc_dir)

            years = solution_paths_by_year.keys()

        if self.config.overwrite_year is not None:
            years = [self.config.overwrite_year]

        is_leaderboard_needed = self.config.what_to_show_on_right_side in [
            "time_and_rank"
        ] or self.config.count_as_solved_when in ["on_leaderboard", "both", "either"]

        solve_data = SolveData({})

        for year in years:
            day_to_solution = solution_paths_by_year.get(year, {})
            day_to_scores = {}
            if is_leaderboard_needed:
                day_to_scores = request_leaderboard(year, self.config)

            day_is_solved = set()

            for day in range(1, 26):
                if self._is_solved(day_to_scores.get(day), day_to_solution.get(day)):
                    day_is_solved.add(day)

            solve_data.year_to_data[year] = YearData(day_to_scores, day_to_solution, day_is_solved)
        return solve_data

    def handle_day(
        self,
        day: int,
        year: int,
        solutions: List[Path],
        html: HTML,
        day_scores: Optional[DayScores],
        needs_update: bool,
        is_solved: bool,
    ):
        languages = []
        for solution in solutions:
            extension = solution.suffix
            if extension in extension_to_colors() and extension not in languages:
                languages.append(extension)
        solution_link = solutions[0] if solutions else None
        day_graphic_path = self.config.image_dir / f"{year:04}/{day:02}.png"
        day_graphic_path.parent.mkdir(parents=True, exist_ok=True)
        if not day_graphic_path.exists() or needs_update:
            self.tile_drawer.draw_tile(f"{day:02}", languages, day_scores, day_graphic_path, is_solved=is_solved)
        day_graphic_path = day_graphic_path.relative_to(self.config.aoc_dir)
        with html.tag("a", href=str(solution_link)):
            html.tag("img", closing=False, src=day_graphic_path.as_posix(), width=self.config.tile_width_px)

    def fill_empty_days_in_dict(self, day_to_solutions: Dict[int, List[Path]], max_day) -> None:
        if not self.config.create_all_days and len(day_to_solutions) == 0:
            print(f"Current year has no solutions!")
        for day in range(1, max_day + 1):
            if day not in day_to_solutions:
                day_to_solutions[day] = []

    def handle_year(self, year: int, year_data: YearData):
        print(f"=== Generating table for year {year} ===")
        leaderboard = year_data.day_to_scores
        day_to_solutions = year_data.day_to_paths
        html = HTML()
        with html.tag("h1", align="center"):
            stars = len(year_data.is_day_solved) * 2
            # stars = sum(
            #     (ds.time1 is not None) + (ds.time2 is not None) for ds in leaderboard.values() if ds is not None
            # )
            html.push(f"{year} - {stars} ⭐")
        max_day = 25 if self.config.create_all_days else max(year_data.is_day_solved)
        self.fill_empty_days_in_dict(day_to_solutions, max_day)

        # completed_solutions = dict()
        # completed_cache_path = self.config.cache_dir / f"completed-{year}.json"
        # if completed_cache_path.exists():
        #     with open(completed_cache_path, "r") as file:
        #         completed_solutions = {int(day): solutions for day, solutions in json.load(file).items()}

        for day in range(1, max_day + 1):
            solutions = day_to_solutions.get(day, [])
            # self.handle_day(day, year, solutions, html, leaderboard.get(day), completed_solutions.get(day) != solutions)
            is_solved = day in year_data.is_day_solved
            self.handle_day(day, year, solutions, html, leaderboard.get(day), True, is_solved=is_solved)

        # with open(completed_cache_path, "w") as file:
        #     completed_days = [day for day, scores in leaderboard.items() if scores.time2 is not None]
        #     file.write(
        #         json.dumps({day: solutions for day, solutions in day_to_solutions.items() if day in completed_days})
        #     )

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

    def make_tiles(self):
        print("Running AoC-Tiles")
        solve_data = self.compose_solve_data()
        with ThreadPoolExecutor(max_workers=1) as executor:  # Use ThreadPoolExecutor or ProcessPoolExecutor
            for year, data in sorted(solve_data.year_to_data.items(), reverse=True):
                executor.submit(self.handle_year, year, data)

        # pprint(solve_data)


def main():
    TileMaker(Config()).make_tiles()
