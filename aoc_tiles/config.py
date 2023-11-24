from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, List, Tuple, Optional

from PIL import ImageColor


@dataclass
class Config:
    aoc_dir: Path = Path("./")
    readme_path: Path = field(init=False)
    session_cookie_path: Path = field(init=False)
    aoc_tiles_dir: Path = field(init=False)
    image_dir: Path = field(init=False)
    cache_dir: Path = field(init=False)

    what_to_show_on_right_parts: Literal["checkmark", "time_and_rank", "loc"] = "checkmark"
    count_as_solved_when: Literal["on_leaderboard", "file_exists", "either", "both"] = "file_exists"
    language_sorting: List[str] = field(default_factory=list)
    separate_files_for_both_parts: bool = False
    create_all_days: bool = False

    year_pattern: str = r'(?<!\d)(20[123]\d)(?!\d)'
    day_pattern: str = r'(?<!\d)([012]?\d)(?!\d)'
    overwrite_ignore_paths: List[Path] = field(default_factory=list)
    overwrite_year: Optional[int] = None

    contrast_improvement_type: Literal["none", "outline", "dark"] = "outline"
    contrast_improvement_threshold: int = 30
    outline_color: Tuple = field(default=ImageColor.getrgb("#6C6A6A"))
    not_completed_color: Tuple = field(default=ImageColor.getrgb("#333333"))
    text_color: Tuple = field(default=ImageColor.getrgb("#FFFFFF"))

    tile_width_px: str = "161px"
    debug: bool = False

    def __post_init__(self):
        self.readme_path = self.aoc_dir / "README.md"
        self.aoc_tiles_dir = self.aoc_dir / ".aoc_tiles"
        self.session_cookie_path = self.aoc_tiles_dir / "session.cookie"
        self.image_dir = self.aoc_tiles_dir / "tiles"
        self.cache_dir = self.aoc_tiles_dir / "cache"


# class Config:
#     def __init__(self):
#         # This results in the parent directory of the script directory, the year directories should be here
#         self.aoc_dir = Path("./")
#
#         # Path to the README file where the tiles should be added
#         self.readme_path = self.aoc_dir / "README.md"
#
#         # Path to the cookie session file
#         self.session_cookie_path = self.aoc_dir / "session.cookie"
#
#         # The directory where all aoc_tiles relevant files will be stored
#         self.aoc_tiles_dir = self.aoc_dir / ".aoc_tiles"
#
#         # The directory where the image files for the tiles are stored. This should be committed to git.
#         # Year directories are created in this directory, then each day is saved as 01.png, 02.png, etc.
#         self.image_dir = self.aoc_tiles_dir / "tiles"
#
#         # Cache path is a subfolder of the AOC folder, it includes the personal leaderboards for each year
#         self.cache_dir = self.aoc_tiles_dir / "cache"
#
#         # Whether the graphic should be created for days that have not been completed yet.
#         # Note that missing days between completed days will still be created.
#         self.create_all_days = False
#
#         # Instead of showing the time and rank you achieved this just shows whether
#         # it was completed with a checkmark
#         self.show_checkmark_instead_of_time_rank = True
#
#         # The year and day pattern to detect directories. For example, if your day folders are
#         # called "day1" to "day25" then set the pattern to r"day\d{1,2}". The script extracts
#         # a number from the folder and tries to guess its day that way.
#         self.year_pattern = r"\d{4}"
#         self.day_pattern = r"\d{1,2}"
#
#         # On how to improve legibility of the text when the background is white, outline will add a dark outline around
#         # the text, "text" will make the text itself dark, none will not change the text color (leaves it white)
#         self.contrast_improvement_type: Literal["none", "outline", "dark"] = "outline"
#
#         # Add outline if too bright ( = too similar to TEXT_WHITE)
#         self.outline_color = ImageColor.getrgb("#6C6A6A")
#         self.contrast_improvement_threshold = 30  # Range from 0 to 255
#
#         # Color if a part is not completed
#         self.not_completed_color = ImageColor.getrgb("#333333")
#         self.text_color = ImageColor.getrgb("#FFFFFF")
#
#         # Width of each tile in the README.md.
#         # 161px is a rather specific number, with it exactly 5 tiles fit into a row. It is possible to go
#         # to 162px, however then 1080p displays show 4 tiles in a row, and phone displays show 1 tile
#         # instead of 2 in a row. Therefore, 161px is used here.
#         self.tile_width_px = "161px"
#
#         # Overrides day 24 part 2 and day 25 both parts to be unsolved
#         self.debug = False
