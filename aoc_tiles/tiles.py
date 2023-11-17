"""
Author: LiquidFun
Source: https://github.com/LiquidFun/adventofcode

To use this script, you need to have a file named
"session.cookie" in the same folder as this script.

It should contain a single line, the "session" cookie
when logged in to https://adventofcode.com. Just
paste it in there.

Then install the requirements as listed in the requirements.txt:
    pip install -r requirements.txt

Then run the script:
    python create_aoc_tiles.py
"""
import functools
import itertools
import math
import time
from collections import namedtuple
from functools import cache
from pathlib import Path
import re
import json
from typing import Literal, Union, List, Dict, Tuple

import requests
from PIL import Image, ImageColor
import yaml
from PIL.ImageDraw import ImageDraw
from PIL import ImageFont

from aoc_tiles.config import Config
from aoc_tiles.html import HTML

# ======================================================
# === The following likely do not need to be changed ===
# ======================================================

# URL for the personal leaderboard (same for everyone)
PERSONAL_LEADERBOARD_URL = "https://adventofcode.com/{year}/leaderboard/self"

# Location of yaml file where file extensions are mapped to colors
GITHUB_LANGUAGES_PATH = Path(__file__).parent / "github_languages.yml"

def get_extension_to_colors():
    extension_to_color = {}
    with open(GITHUB_LANGUAGES_PATH) as file:
        github_languages = yaml.load(file, Loader=yaml.FullLoader)
        for language, data in github_languages.items():
            if "color" in data and "extensions" in data and data["type"] == "programming":
                for extension in data["extensions"]:
                    extension_to_color[extension.lower()] = data["color"]
    return extension_to_color

def darker_color(c: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
    return c[0] - 10, c[1] - 10, c[2] - 10, 255


# Luminance of color
def luminance(color):
    return 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]


# How similar is color_a to color_b
def color_similarity(color_a, color_b, threshold):
    return abs(luminance(color_a) - luminance(color_b)) < threshold



@cache
def get_font(self, size: int, path: str):
    return ImageFont.truetype(str(path), size)

FONTS_PATH = Path(__file__).parent / "resources" / "fonts"

# Fonts, note that the fonts sizes are specifically adjusted to the following fonts, if you change the fonts
# you might need to adjust the font sizes and text locations in the rest of the script.
main_font = functools.partial(get_font, path=FONTS_PATH / "PaytoneOne.ttf")
secondary_font = functools.partial(get_font, path=FONTS_PATH / "SourceCodePro-Regular.otf")

DayScores = namedtuple("DayScores", ["time1", "rank1", "score1", "time2", "rank2", "score2"], defaults=[None] * 3)

class AoCTiles:
    
    def __init__(self, config: Config):
        self.config = config
        self.extension_to_color: Dict[str, str] = get_extension_to_colors()

    # You can change this code entirely, or just change patterns above. You get more control if you change the code.
    def get_solution_paths_dict_for_years(self, aoc_dir: Union[str, Path]) -> Dict[int, Dict[int, List[str]]]:
        """Returns a dictionary which maps years to days to a list of solution paths,

        E.g.: {2022: {1: [Path("2022/01/01.py"), Path("2022/01/01.kt")], ...}}

        This functions gives you more control of which solutions should be shown in the tiles. For example, you
        can filter by extension, or only show a single solution, or show tiles for days that have been completed
        but do not have a solution.

        These can also be links to external solutions, e.g. if you want to show a solution from a different repository.
        (Untested however)

        """
        solution_paths_dict: Dict[int, Dict[int, List[str]]] = {}

        def find_first_number(string: str) -> int:
            return int(re.findall(r"\d+", string)[0])

        # If you use a new repo for years you might just remove this if, and assign the year manually
        matching_paths = self.get_paths_matching_regex(self.config.aoc_dir, self.config.year_pattern)
        for year_dir in sorted(matching_paths, reverse=True):
            year = find_first_number(year_dir.name)
            solution_paths_dict[year] = {}
            # If you have a deep structure then you can adjust the year dir as well:
            # year_dir = year_dir / "src/main/kotlin/com/example/aoc"
            for day_dir in self.get_paths_matching_regex(year_dir, self.config.day_pattern):
                day = find_first_number(day_dir.name)
                solutions = sorted(self.find_recursive_solution_files(day_dir))

                # To filter by extension:
                # solutions = [s for s in solutions if s.suffix == ".py"]

                # To only show a single solution:
                # solutions = [solutions[0]]

                # To show tiles for days that have been completed but do not have a solution:
                # if len(solutions) == 0:
                #     solutions = [Path("dummy.kt")]

                solutions = [solution.relative_to(self.config.aoc_dir) for solution in solutions]

                solution_paths_dict[year][day] = [s.as_posix() for s in solutions]
        return solution_paths_dict



    def get_paths_matching_regex(self, path: Path, pattern: str):
        return sorted([p for p in path.iterdir() if re.fullmatch(pattern, p.name)])


    def find_recursive_solution_files(self, directory: Path) -> List[Path]:
        solution_paths = []
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix in self.extension_to_color:
                solution_paths.append(path)
        return solution_paths


    def parse_leaderboard(self, leaderboard_path: Path) -> Dict[int, DayScores]:
        no_stars = "You haven't collected any stars... yet."
        start = '<span class="leaderboard-daydesc-both"> *Time *Rank *Score</span>\n'
        end = "</pre>"
        with open(leaderboard_path) as file:
            html = file.read()
            if no_stars in html:
                return {}
            matches = re.findall(rf"{start}(.*?){end}", html, re.DOTALL | re.MULTILINE)
            assert len(matches) == 1, f"Found {'no' if len(matches) == 0 else 'more than one'} leaderboard?!"
            table_rows = matches[0].strip().split("\n")
            leaderboard = {}
            for line in table_rows:
                day, *scores = re.split(r"\s+", line.strip())
                # replace "-" with None to be able to handle the data later, like if no score existed for the day
                scores = [s if s != "-" else None for s in scores]
                assert len(scores) in (3, 6), f"Number scores for {day=} ({scores}) are not 3 or 6."
                leaderboard[int(day)] = DayScores(*scores)
            return leaderboard


    def request_leaderboard(self, year: int) -> Dict[int, DayScores]:
        leaderboard_path = self.config.cache_dir / f"leaderboard{year}.html"
        if leaderboard_path.exists():
            leaderboard = self.parse_leaderboard(leaderboard_path)
            less_than_30mins = time.time() - leaderboard_path.lstat().st_mtime < 60 * 30
            if less_than_30mins:
                print(f"Leaderboard for {year} is younger than 30 minutes, skipping download in order to avoid DDOS.")
                return leaderboard
            has_no_none_values = all(itertools.chain(map(list, leaderboard.values())))
            if has_no_none_values and len(leaderboard) == 25:
                print(f"Leaderboard for {year} is complete, no need to download.")
                return leaderboard
        with open(self.config.session_cookie_path) as cookie_file:
            session_cookie = cookie_file.read().strip()
            assert len(session_cookie) == 128, f"Session cookie is not 128 characters long, make sure to remove the prefix!"
            data = requests.get(
                PERSONAL_LEADERBOARD_URL.format(year=year),
                headers={"User-Agent": "https://github.com/LiquidFun/adventofcode by Brutenis Gliwa"},
                cookies={"session": session_cookie},
            ).text
            leaderboard_path.parent.mkdir(exist_ok=True, parents=True)
            with open(leaderboard_path, "w") as file:
                file.write(data)
        return self.parse_leaderboard(leaderboard_path)





    def get_alternating_background(self, languages, both_parts_completed=True, *, stripe_width=20):
        colors = [ImageColor.getrgb(self.extension_to_color[language]) for language in languages]
        if len(colors) == 1:
            colors.append(darker_color(colors[0]))
        image = Image.new("RGB", (200, 100), self.config.not_completed_color)

        def fill_with_colors(colors, fill_only_half):
            for x in range(image.width):
                for y in range(image.height):
                    if fill_only_half and x / image.width + y / image.height > 1:
                        continue
                    image.load()[x, y] = colors[((x + y) // stripe_width) % len(colors)]

        fill_with_colors([self.config.not_completed_color, darker_color(self.config.not_completed_color)], False)
        if colors:
            fill_with_colors(colors, not both_parts_completed)
        return image


    def format_time(self, time: str) -> str:
        """Formats time as mm:ss if the time is below 1 hour, otherwise it returns >1h to a max of >24h

        >>> format_time("00:58:32")
        '58:32'
        >>> format_time(">1h")
        '  >1h'
        """
        time = time.replace("&gt;", ">")
        if ">" in time:
            formatted = time
        else:
            h, m, s = time.split(":")
            formatted = f">{h}h" if int(h) >= 1 else f"{m:02}:{s:02}"
        return f"{formatted:>5}"


    def draw_star(self, drawer: ImageDraw, at: Tuple[int, int], size=9, color="#ffff0022", num_points=5):
        """Draws a star at the given position"""
        diff = math.pi * 2 / num_points / 2
        points: List[Tuple[float, float]] = []
        for angle in [diff * i - math.pi / 2 for i in range(num_points * 2)]:
            factor = size if len(points) % 2 == 0 else size * 0.4
            points.append((at[0] + math.cos(angle) * factor, at[1] + math.sin(angle) * factor))
        drawer.polygon(points, fill=color)


    def generate_day_tile_image(self, day: str, year: str, languages: List[str], day_scores: DayScores | None, path: Path):
        """Saves a graphic for a given day and year. Returns the path to it."""
        image = self.get_alternating_background(languages, not (day_scores is None or day_scores.time2 is None))
        drawer = ImageDraw(image)
        text_kwargs = {"fill": self.config.text_color}

        # Get all colors of the day, check if any one is similar to TEXT_COLOR
        # If yes, add outline
        for language in languages:
            color = ImageColor.getrgb(self.extension_to_color[language])
            if color_similarity(color, self.config.text_color, self.config.contrast_improvement_threshold):
                if "outline" in self.config.contrast_improvement_type:
                    text_kwargs["stroke_width"] = 1
                    text_kwargs["stroke_fill"] = self.config.outline_color
                if "dark" in self.config.contrast_improvement_type:
                    text_kwargs["fill"] = self.config.not_completed_color
                break

        font_color = text_kwargs["fill"]

        # === Left side ===
        drawer.text((3, -5), "Day", align="left", font=main_font(20), **text_kwargs)
        drawer.text((1, -10), str(day), align="center", font=main_font(75), **text_kwargs)
        # Calculate font size based on number of characters, because it might overflow
        lang_as_str = " ".join(languages)
        lang_font_size = max(6, int(18 - max(0, len(lang_as_str) - 8) * 1.3))
        drawer.text((0, 74), lang_as_str, align="left", font=secondary_font(lang_font_size), **text_kwargs)

        # === Right side (P1 & P2) ===
        for part in (1, 2):
            y = 50 if part == 2 else 0
            time, rank = getattr(day_scores, f"time{part}", None), getattr(day_scores, f"rank{part}", None)
            if day_scores is not None and time is not None:
                drawer.text((104, -5 + y), f"P{part} ", align="left", font=main_font(25), **text_kwargs)
                if self.config.show_checkmark_instead_of_time_rank:
                    drawer.line((160, 35 + y, 150, 25 + y), fill=font_color, width=2)
                    drawer.line((160, 35 + y, 180, 15 + y), fill=font_color, width=2)
                    continue
                drawer.text((105, 25 + y), "time", align="right", font=secondary_font(10), **text_kwargs)
                drawer.text((105, 35 + y), "rank", align="right", font=secondary_font(10), **text_kwargs)
                drawer.text((143, 3 + y), self.format_time(time), align="right", font=secondary_font(18), **text_kwargs)
                drawer.text((133, 23 + y), f"{rank:>6}", align="right", font=secondary_font(18), **text_kwargs)
            else:
                drawer.line((140, 15 + y, 160, 35 + y), fill=font_color, width=2)
                drawer.line((140, 35 + y, 160, 15 + y), fill=font_color, width=2)

        if day_scores is None and not languages:
            drawer.line((15, 85, 85, 85), fill=self.config.text_color, width=2)

        # === Divider lines ===
        drawer.line((100, 5, 100, 95), fill=font_color, width=1)
        drawer.line((105, 50, 195, 50), fill=font_color, width=1)

        image.save(path)


    def handle_day(self, day: int, year: int, solutions: List[str], html: HTML, day_scores: DayScores | None, needs_update: bool):
        languages = []
        for solution in solutions:
            extension = "." + solution.split(".")[-1]
            if extension in self.extension_to_color and extension not in languages:
                languages.append(extension)
        solution_link = solutions[0] if solutions else None
        if self.config:
            if day == 25:
                languages = []
        day_graphic_path = self.config.image_dir / f"{year:04}/{day:02}.png"
        day_graphic_path.parent.mkdir(parents=True, exist_ok=True)
        if not day_graphic_path.exists() or needs_update:
            self.generate_day_tile_image(f"{day:02}", f"{year:04}", languages, day_scores, day_graphic_path)
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
        leaderboard = self.request_leaderboard(year)
        if self.config.debug:
            leaderboard[25] = None
            leaderboard[24] = DayScores("22:22:22", "12313", "0")
            day_to_solutions[23] = []
        html = HTML()
        with html.tag("h1", align="center"):
            stars = sum((ds.time1 is not None) + (ds.time2 is not None) for ds in leaderboard.values() if ds is not None)
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
            file.write(json.dumps({day: solutions for day, solutions in day_to_solutions.items() if day in completed_days}))

        with open(self.config.readme_path, "r", encoding="utf-8") as file:
            text = file.read()
            begin = "<!-- AOC TILES BEGIN -->"
            end = "<!-- AOC TILES END -->"
            assert begin in text and end in text, f"Could not find AOC TILES markers '{begin}' and '{end}' in the " \
                                                  f"README.md! Make sure to add them to the README at {self.config.readme_path}."
            pattern = re.compile(rf"{begin}.*{end}", re.DOTALL | re.MULTILINE)
            new_text = pattern.sub(f"{begin}\n{html}\n{end}", text)

        with open(self.config.readme_path, "w", encoding="utf-8") as file:
            file.write(str(new_text))


    def run(self):
        print("Running aoc-tiles")
        for year, day_to_solutions_list in self.get_solution_paths_dict_for_years().items():
            print(f"=== Generating table for year {year} ===")
            self.handle_year(year, day_to_solutions_list)

def main():
    config = Config()
    AoCTiles(config).run()


if __name__ == "__main__":
    main()
