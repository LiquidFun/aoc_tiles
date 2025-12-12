import re
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import List, Dict

import git
from git import GitCommandError, InvalidGitRepositoryError
from loguru import logger

from aoc_tiles.colors import extension_to_colors
from aoc_tiles.config import Config


class SolutionFinder:
    def __init__(self, config: Config):
        self.config = config
        try:
            self.repository = git.Repo(config.aoc_dir)
        except InvalidGitRepositoryError:
            print(f"{config.aoc_dir} is an InvalidGitRepository. Git functionality will not be available.")
            self.repository = None

        if self.config.session_cookie_path.exists():
            msg = f"This is a security risk! Ensure that the {self.config.session_cookie_path} "
            if self.git_is_file_tracked(self.config.session_cookie_path):
                msg += "file is not tracked by git!"
                exit(f"[ERROR] Session cookie file is tracked by git. {msg} Aborting!")
            elif not self.git_is_file_ignored(self.config.session_cookie_path):
                msg += " is in your .gitignore!"
                print(f"[WARNING] Session cookie file is not git ignored. {msg}")

    def get_solution_paths_by_year(self, aoc_dir: Path) -> Dict[int, Dict[int, List[Path]]]:
        day_to_solution_paths = defaultdict(lambda: defaultdict(list))
        year_pattern = re.compile(self.config.year_pattern)
        day_pattern = re.compile(self.config.day_pattern)
        logger.debug("Finding solution files recursively in {}", aoc_dir)
        candidate_paths = sorted(self._find_recursive_solution_files(aoc_dir))
        logger.debug("Candidate paths: {}", candidate_paths)
        for path in candidate_paths:
            years = year_pattern.findall(path.as_posix())
            days = day_pattern.findall(path.as_posix())
            year = None
            if years:
                year = int(years[-1])
            if self.config.overwrite_year is not None:
                year = self.config.overwrite_year
            if year is not None and days:
                day_to_solution_paths[year][int(days[0])].append(path)

        self._ensure_sorting(day_to_solution_paths)
        # pprint(day_to_solution_paths)
        return day_to_solution_paths

    def _ensure_sorting(self, solution_paths_dict: Dict[int, Dict[int, List[str]]]) -> Dict[int, Dict[int, List[str]]]:
        def sort_key(path: Path):
            suffix = path.suffix.lower()
            if suffix in self.config.language_sorting:
                return self.config.language_sorting.index(suffix), suffix
            return 99999, suffix

        for year in solution_paths_dict:
            for day in solution_paths_dict[year]:
                solution_paths_dict[year][day] = sorted(solution_paths_dict[year][day], key=sort_key)
        return solution_paths_dict

    def _find_recursive_solution_files(self, directory: Path) -> List[Path]:
        if self.config.only_use_solutions_in_git and self.repository is not None:
            files = [Path(s) for s in self.git_get_tracked_files()]
        else:
            files = list(directory.rglob("*"))

        logger.debug("Found {} files", len(files))
        logger.trace(f"Files: {files}")
        solution_paths = []
        for path in files:
            extension_is_supported = path.suffix in extension_to_colors()
            path_is_excluded = any([path.match(exclude) for exclude in self.config.exclude_patterns])
            if path_is_excluded:
                logger.debug(
                    "Excluded: {} because of patterns: {}",
                    path,
                    self.config.exclude_patterns,
                )
            if path.is_file() and extension_is_supported and not path_is_excluded:
                solution_paths.append(path)
        logger.debug("Found {} solution files", len(solution_paths))
        logger.trace("Solution files:", "\n".join(map(str, solution_paths)))
        return solution_paths

    def git_is_file_ignored(self, filepath):
        if self.repository is None:
            return False
        try:
            self.repository.git.execute(["git", "check-ignore", "-q", str(filepath)])
            return True
        except GitCommandError:
            return False

    @lru_cache
    def git_get_tracked_files(self) -> List[str]:
        if self.repository is None:
            return []
        return self.repository.git.ls_files().split("\n")

    def git_is_file_tracked(self, filepath: Path):
        tracked_files = self.git_get_tracked_files()
        return str(filepath) in tracked_files

    def git_add(self, path: Path):
        if self.repository is not None and path.exists():
            self.repository.git.add(str(path))

    def git_commit_amend(self):
        # Command based on this:
        # https://stackoverflow.com/questions/3284292/can-a-git-hook-automatically-add-files-to-the-commit
        if self.repository is not None:
            self.repository.git.commit("--amend", "-C", "HEAD", "--no-verify")


def main():
    SolutionFinder(Config()).get_solution_paths_by_year(Path())


if __name__ == "__main__":
    main()
