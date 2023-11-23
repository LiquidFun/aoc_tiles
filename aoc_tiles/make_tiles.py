from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Set, List

from aoc_tiles.config import Config
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

    def make_tiles(self):
        solution_finder = SolutionFinder(self.config)
        solution_finder.get_solution_paths_by_year(self.config.aoc_dir)

        is_leaderboard_needed = (
            self.config.what_to_show_on_right_parts == 'time_and_rank'
            or self.config.count_as_solved_when in ['on_leaderboard', 'both', "either"]
        )
        if is_leaderboard_needed:
            leaderboard = request_leaderboard(2022, self.config)