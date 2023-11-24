from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
from typing import Dict, Set, List, Optional

from aoc_tiles.config import Config
from aoc_tiles.drawer import TileDrawer
from aoc_tiles.leaderboard import DayScores, request_leaderboard
from aoc_tiles.solutions import SolutionFinder


@dataclass
class SolveDataForYear:
    day_to_scores: Dict[int, DayScores]
    day_to_paths: Dict[int, List[Path]]
    is_day_solved: Set[int]

@dataclass
class SolveData:
    year_to_data: Dict[int, SolveDataForYear]


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


    def compose_solve_data(self):
        is_solution_paths_needed = (
                self.config.what_to_show_on_right_parts in ['loc']
                or self.config.count_as_solved_when in ['file_exists', 'both', "either"]
        )
        solution_paths_by_year = {}
        years = []
        if is_solution_paths_needed:
            solution_finder = SolutionFinder(self.config)
            solution_paths_by_year = solution_finder.get_solution_paths_by_year(self.config.aoc_dir)

            years = solution_paths_by_year.keys()

        if self.config.overwrite_year is not None:
            years = [self.config.overwrite_year]

        is_leaderboard_needed = (
                self.config.what_to_show_on_right_parts in ['time_and_rank']
                or self.config.count_as_solved_when in ['on_leaderboard', 'both', "either"]
        )

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

            solve_data.year_to_data[year] = SolveDataForYear(day_to_scores, day_to_solution, day_is_solved)
        return solve_data

    def make_tiles(self):
        solve_data = self.compose_solve_data()
        self.tile_drawer.draw_tile()

        pprint(solve_data)



def main():
    TileMaker(Config()).make_tiles()