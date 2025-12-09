import itertools
import re
import time
from dataclasses import dataclass, fields
from datetime import datetime, timezone
from pathlib import Path
from typing import Union, Dict, List, Set

from loguru import logger
import requests

from aoc_tiles.config import Config

# URL for the personal leaderboard (same for everyone)
PERSONAL_LEADERBOARD_URL = "https://adventofcode.com/{year}/leaderboard/self"


@dataclass
class DayScores:
    time1: Union[str, None] = None
    rank1: Union[str, None] = None
    score1: Union[str, None] = None
    time2: Union[str, None] = None
    rank2: Union[str, None] = None
    score2: Union[str, None] = None


def _parse_leaderboard(leaderboard_path: Path) -> Dict[int, DayScores]:
    no_stars = "You haven't collected any stars... yet."
    start = r'<span class="leaderboard-daydesc-both">(?: *Time *Rank *Score|-Part 2-)</span>\n'
    end = "</pre>"
    with open(leaderboard_path) as file:
        html = file.read()
        logger.debug(f"Found html file: {leaderboard_path}")
        logger.trace(f"With contents: {html}")
        if no_stars in html:
            return {}
        matches = re.findall(rf"{start}(.*?){end}", html, re.DOTALL | re.MULTILINE)
        assert len(matches) == 1, f"Found {'no' if len(matches) == 0 else 'more than one'} leaderboard?!"
        table_rows = matches[0].strip().split("\n")
        day_to_scores = {}
        for line in table_rows:
            day, *scores = re.split(r"\s+", line.strip())
            if len(scores) in (1, 2):
                # In year 2025 there is no longer any info about rank/score, therefore we just pad it with None
                if len(scores) == 1:
                    scores.append(None)
                scores = [scores[0], None, None, scores[1], None, None]
            # replace "-" with None to be able to handle the data later, like if no score existed for the day
            scores = [s if s != "-" else None for s in scores]
            assert len(scores) in (3, 6), f"Number scores for {day=} ({scores}) are not 3 or 6."
            day_to_scores[int(day)] = DayScores(*scores)
        return day_to_scores


def _is_year_already_unlocked(year: int) -> bool:
    unlock_time = datetime(year, 12, 1, 5, 0, tzinfo=timezone.utc)
    curr_time = datetime.now(timezone.utc)
    return unlock_time <= curr_time


def request_leaderboard(year: int, config: Config) -> Dict[int, DayScores]:
    leaderboard_path = config.cache_dir / f"leaderboard{year}.html"

    if not _is_year_already_unlocked(year):
        print(f"Advent of Code {year} has not unlocked yet, skipping leaderboard retrieval.")
        return {}

    if leaderboard_path.exists():
        leaderboard = _parse_leaderboard(leaderboard_path)
        less_than_30mins = time.time() - leaderboard_path.lstat().st_mtime < 60 * 30
        if less_than_30mins:
            print(f"Leaderboard for {year} is younger than 30 minutes, skipping download in order to avoid DDOS.")
            return leaderboard
        has_no_none_values = all(itertools.chain(map(fields, leaderboard.values())))
        if has_no_none_values and len(leaderboard) == 25:
            print(f"Leaderboard for {year} is complete, no need to download.")
            return leaderboard

    with open(config.session_cookie_path) as cookie_file:
        session_cookie = cookie_file.read().strip()
        assert len(session_cookie) == 128, f"Session cookie is not 128 characters long, make sure to remove the prefix!"
        data = requests.get(
            PERSONAL_LEADERBOARD_URL.format(year=year),
            headers={"User-Agent": "https://github.com/LiquidFun/aoc_tiles by Brutenis Gliwa"},
            cookies={"session": session_cookie},
        ).text
        leaderboard_path.parent.mkdir(exist_ok=True, parents=True)
        with open(leaderboard_path, "w") as file:
            file.write(data)
    return _parse_leaderboard(leaderboard_path)
