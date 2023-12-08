from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, List, Tuple, Optional, Union

from PIL import ImageColor


@dataclass
class Config:
    aoc_dir: Union[str, Path] = field(default="./", metadata={"help": "Path to the AoC directory.", "type": str})
    readme_path: Union[str, Path] = field(init=False)
    session_cookie_path: Union[str, Path] = field(init=False)
    aoc_tiles_dir: Union[str, Path] = field(init=False)
    image_dir: Union[str, Path] = field(init=False)
    cache_dir: Union[str, Path] = field(init=False)

    verbose: bool = field(default=False, metadata={"help": "Whether to print debug information."})

    what_to_show_on_right_side: Literal["checkmark", "time_and_rank", "loc"] = field(
        default="checkmark", metadata={"help": "What information to display on the right side of each tile."}
    )
    count_as_solved_when: Literal["on_leaderboard", "file_exists", "either", "both"] = field(
        default="file_exists",
        metadata={
            "help": "Condition to count a task as solved. Note that 'on_leaderboard', 'either' and 'both' require a "
                    "session cookie."
        },
    )
    language_sorting: List[str] = field(
        default_factory=list,
        metadata={
            "help": "Preferred language extensions order for sorting. For example 'py,rs,js' will make Python "
                    "solutions appear first, then Rust, then JavaScript, then everything else (alphabetically)."
        },
    )
    only_use_git_files: bool = field(default=True, metadata={
        "help": "Whether to only use files tracked by git, i.e. files in .gitignore are skipped."})
    create_all_days: bool = field(default=False, metadata={"help": "Whether to create entries for all days upfront."})

    year_pattern: str = field(
        default=r"(?<!\d)(20[123]\d)(?!\d)",
        metadata={
            "help": "Regex pattern for matching years. This extracts the first group as the year and parses it as an "
                    "integer. Make sure that other numbers are not matched by this pattern! For example, "
                    "using negative lookbehind and lookaheads is encouraged to avoid matching longer numbers!"
        },
    )
    day_pattern: str = field(
        default=r"(?<!\d)([012]?\d)(?!\d)", metadata={"help": "Regex pattern for matching days. Same as year_pattern."}
    )
    overwrite_ignore_paths: List[Union[str, Path]] = field(
        default_factory=list, metadata={"help": "A list of paths to ignore when looking for solutions"}
    )
    overwrite_year: Optional[int] = field(
        default=None,
        metadata={
            "help": "If your repository only contains a single year and it cannot be parsed from the path, then you "
                    "should use this to overwrite the year. Every solution is presumed to be for this year."
        },
    )

    contrast_improvement_type: Literal["none", "outline", "dark"] = field(
        default="outline",
        metadata={
            "help": "Some languages have very light colors and are hard to see with a white font. Here you can choose "
                    "how the text color changes when the background is too light. 'dark' makes the font dark, "
                    "'outline' adds a black outline."
        },
    )
    contrast_improvement_threshold: int = field(
        default=30, metadata={"help": "Threshold for contrast improvement feature (between 0 and 255)."}
    )
    outline_color: Union[str, Tuple] = field(
        default="#6C6A6A", metadata={"help": "Color used for outlining elements.", "type": str}
    )
    not_completed_color: Union[str, Tuple] = field(
        default="#333333", metadata={"help": "Color to signify incomplete tasks.", "type": str}
    )
    text_color: Union[str, Tuple] = field(default="#FFFFFF", metadata={"help": "Text color.", "type": str})

    tile_width_px: str = field(default="161px", metadata={"help": "Width of tiles in pixels."})
    debug: bool = field(default=False, metadata={"help": "Enable debug mode."})

    def __post_init__(self):
        self.aoc_dir = Path(self.aoc_dir)

        if not hasattr(self, "readme_path"):
            self.readme_path = self.aoc_dir / "README.md"

        if not hasattr(self, "aoc_tiles_dir"):
            self.aoc_tiles_dir = self.aoc_dir / ".aoc_tiles"

        if not hasattr(self, "session_cookie_path"):
            self.session_cookie_path = self.aoc_tiles_dir / "session.cookie"
            if not self.session_cookie_path.exists():
                self.session_cookie_path = self.aoc_dir / "session.cookie"

        if not hasattr(self, "image_dir"):
            self.image_dir = self.aoc_tiles_dir / "tiles"

        if not hasattr(self, "cache_dir"):
            self.cache_dir = self.aoc_tiles_dir / "cache"

        self.outline_color = ImageColor.getrgb(self.outline_color)
        self.not_completed_color = ImageColor.getrgb(self.not_completed_color)
        self.text_color = ImageColor.getrgb(self.text_color)

        for i, suffix in enumerate(self.language_sorting):
            if not suffix.startswith("."):
                self.language_sorting[i] = "." + suffix

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
