import re
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import datetime
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger

from aoc_tiles.colors import extension_to_colors, extension_to_programming_language
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
    day_to_stars: Dict[int, int]


@dataclass
class SolveData:
    year_to_data: Dict[int, YearData]


class TileMaker:
    def __init__(self, config: Config):
        self.config = config
        self.tile_drawer = TileDrawer(config)
        self.solution_finder = SolutionFinder(config)

    def _get_stars(self, solved: DayScores, solution: List[Path]):
        on_leaderboard = 0 if solved is None else bool(solved.time1) + bool(solved.time2)
        file_exists = 0 if solution is None else 2
        return {
            "on_leaderboard": on_leaderboard,
            "file_exists": file_exists,
            "either": max(on_leaderboard, file_exists),
            "both": min(on_leaderboard, file_exists),
        }[self.config.count_as_solved_when]

    def compose_solve_data(self) -> SolveData:
        solution_paths_by_year = self.solution_finder.get_solution_paths_by_year(self.config.aoc_dir)
        years = solution_paths_by_year.keys()

        is_leaderboard_needed = self.config.what_to_show_on_right_side in [
            "time_and_rank"
        ] or self.config.count_as_solved_when in ["on_leaderboard", "both", "either"]

        solve_data = SolveData({})

        for year in years:
            day_to_solution = solution_paths_by_year.get(year, {})
            day_to_scores = {}
            if is_leaderboard_needed:
                logger.debug("Requesting leaderboard for year {}", year)
                day_to_scores = request_leaderboard(year, self.config)

            day_to_stars = {}

            for day in range(1, 26):
                stars = self._get_stars(day_to_scores.get(day), day_to_solution.get(day))
                day_to_stars[day] = stars

            solve_data.year_to_data[year] = YearData(day_to_scores, day_to_solution, day_to_stars)
        return solve_data

    def handle_day(
        self,
        day: int,
        year: int,
        solutions: List[Path],
        day_scores: Optional[DayScores],
        needs_update: bool,
        stars: int,
    ):
        logger.debug("day={} year={} solutions={}", day, year, solutions)
        languages = []
        for solution in solutions:
            extension = solution.suffix
            if extension in extension_to_colors() and extension not in languages:
                languages.append(extension)
        solution_link = solutions[0] if solutions else None
        img_extension = ".gif" if self.config.animation != "none" else ".png"
        day_graphic_path = self.config.image_dir / f"{year:04}/{day:02}{img_extension}"
        day_graphic_path.parent.mkdir(parents=True, exist_ok=True)
        if not day_graphic_path.exists() or needs_update:
            self.tile_drawer.draw_tile(f"{day:02}", languages, day_scores, day_graphic_path, stars=stars)
        day_graphic_path = day_graphic_path.relative_to(self.config.aoc_dir)
        return day_graphic_path, solution_link

    def fill_empty_days_in_dict(self, day_to_solutions: Dict[int, List[Path]], max_day) -> None:
        if not self.config.create_all_days and len(day_to_solutions) == 0:
            print("Current year has no solutions!")
        for day in range(1, max_day + 1):
            if day not in day_to_solutions:
                day_to_solutions[day] = []

    def _get_programming_languages_used_daily(self, year_data: YearData) -> List[str]:
        extensions = None
        for paths in year_data.day_to_paths.values():
            suffixes = {path.suffix for path in paths}
            if extensions is None:
                extensions = suffixes
            extensions &= suffixes

        return [extension_to_programming_language()[extension] for extension in extensions]

    def handle_year(self, year: int, year_data: YearData, html: HTML):
        print(f"=== Generating table for year {year} ===")
        leaderboard = year_data.day_to_scores
        day_to_solutions = year_data.day_to_paths
        with html.tag("h1", align="center"):
            stars = sum(year_data.day_to_stars.values())
            daily_language = " - " + "/".join(self._get_programming_languages_used_daily(year_data))
            html.push(f"{year} - {stars} ⭐{daily_language}")
        max_solved_day = max(
            (day for day, stars in year_data.day_to_stars.items() if stars > 0),
            default=0,
        )
        max_day = 25 if self.config.create_all_days else max_solved_day
        self.fill_empty_days_in_dict(day_to_solutions, max_day)

        # completed_solutions = dict()
        # completed_cache_path = self.config.cache_dir / f"completed-{year}.json"
        # if completed_cache_path.exists():
        #     with open(completed_cache_path, "r") as file:
        #         completed_solutions = {int(day): solutions for day, solutions in json.load(file).items()}

        day_to_future = {}
        with ProcessPoolExecutor() as executor:
            for day in range(1, max_day + 1):
                solutions = day_to_solutions.get(day, [])
                stars = year_data.day_to_stars[day]
                future = executor.submit(
                    self.handle_day,
                    day,
                    year,
                    solutions,
                    leaderboard.get(day),
                    True,
                    stars=stars,
                )
                day_to_future[day] = future

        for day, future in day_to_future.items():
            tile_path, solution_path = future.result()

            if solution_path is None:
                solution_href = str(solution_path)
            else:
                solution_href = str(solution_path.as_posix())

            with html.tag("a", href=solution_href):
                html.tag(
                    "img",
                    closing=False,
                    src=tile_path.as_posix(),
                    width=self.config.tile_width_px,
                )

        # with open(completed_cache_path, "w") as file:
        #     completed_days = [day for day, scores in leaderboard.items() if scores.time2 is not None]
        #     file.write(
        #         json.dumps({day: solutions for day, solutions in day_to_solutions.items() if day in completed_days})
        #     )

    def _ensure_is_not_running_already(self):
        if self.config.aoc_tiles_dir.exists():
            if self.config.running_lock_path in self.config.aoc_tiles_dir.iterdir():
                print("AoC-Tiles is already running! Remove running.lock if this is not the case.")
                exit()

    def _write_to_readme(self, html: HTML):
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

    @staticmethod
    def _get_total_possible_stars_for_date(utc_date: datetime.datetime):
        total = 0
        for year in range(2015, utc_date.year + 2):
            for day in range(1, 26):
                unlock_time = datetime.datetime(year, 12, day, 0, 0, 0, 0, tzinfo=datetime.timezone.utc)
                if utc_date >= unlock_time:
                    total += 2
        return total

    def _add_total_completed_stars_to_html(self, solve_data: SolveData, html: HTML):
        add_header = (
            self.config.show_total_stars_for_all_years == "yes"
            or self.config.show_total_stars_for_all_years == "auto"
            and len(solve_data.year_to_data) >= 3
        )
        if add_header:
            total_stars = sum(sum(data.day_to_stars.values()) for data in solve_data.year_to_data.values())
            total_possible_stars = self._get_total_possible_stars_for_date(datetime.datetime.now(datetime.timezone.utc))
            with html.tag("h1", align="center"):
                html.push(f"Advent of Code - {total_stars}/{total_possible_stars} ⭐")

    def make_tiles(self):
        self._ensure_is_not_running_already()
        print("Running AoC-Tiles")
        solve_data = self.compose_solve_data()
        logger.info("Found {} years with solutions", len(solve_data.year_to_data))
        html = HTML()
        self._add_total_completed_stars_to_html(solve_data, html)

        for year, data in sorted(solve_data.year_to_data.items(), reverse=True):
            logger.debug("year={} data={}", year, data)
            self.handle_year(year, data, html)

        self._write_to_readme(html)

        if self.config.auto_add_tiles_to_git in ["add", "amend"]:
            self.solution_finder.git_add(self.config.image_dir)
            self.solution_finder.git_add(self.config.readme_path)

        if self.config.auto_add_tiles_to_git in ["amend"]:
            try:
                with open(self.config.running_lock_path, "w") as file:
                    file.write("")
                self.solution_finder.git_commit_amend()
            finally:
                # print("Could not amend commit. Maybe there is nothing to amend?")
                if self.config.running_lock_path.exists():
                    self.config.running_lock_path.unlink()


def main():
    TileMaker(Config()).make_tiles()
