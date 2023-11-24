import re
from collections import defaultdict
from pathlib import Path
from pprint import pprint
from typing import List, Dict, Optional

from aoc_tiles.colors import extension_to_colors
from aoc_tiles.config import Config


class SolutionFinder:

    def __init__(self, config: Config):
        self.config = config

    def get_solution_paths_by_year(self, aoc_dir: Path) -> Dict[Optional[int], Dict[int, List[Path]]]:
        day_to_solution_paths = defaultdict(lambda: defaultdict(list))
        year_pattern = re.compile(self.config.year_pattern)
        day_pattern = re.compile(self.config.day_pattern)
        for path in sorted(self._find_recursive_solution_files(aoc_dir)):
            years = year_pattern.findall(str(path))
            days = day_pattern.findall(str(path))
            if not years:
                years.append(None)
            for year in years:
                if days:
                    day_to_solution_paths[year][int(days[0])].append(path)

        self._ensure_sorting(day_to_solution_paths)
        pprint(day_to_solution_paths)
        return day_to_solution_paths

    def _ensure_sorting(self, solution_paths_dict: Dict[int, Dict[int, List[str]]]) -> Dict[int, Dict[int, List[str]]]:
        def sort_key(path: Path):
            suffix = path.suffix.lower()
            if suffix in self.config.language_sorting:
                return f"{self.config.language_sorting.index(suffix):05}_{suffix}"
            return '99999_' + suffix

        for year in solution_paths_dict:
            for day in solution_paths_dict[year]:
                solution_paths_dict[year][day] = sorted(solution_paths_dict[year][day], key=sort_key)
        return solution_paths_dict

    def _find_recursive_solution_files(self, directory: Path) -> List[Path]:
        solution_paths = []
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix in extension_to_colors():
                solution_paths.append(path)
        return solution_paths


def main():
    SolutionFinder(Config()).get_solution_paths_by_year(Path())


if __name__ == '__main__':
    main()
