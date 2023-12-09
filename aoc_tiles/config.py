import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, List, Tuple, Optional, Union

from PIL import ImageColor
from loguru import logger


@dataclass
class Config:
    aoc_dir: Union[str, Path] = field(default="./", metadata={"help": "Path to the AoC directory.", "type": str})
    readme_path: Union[str, Path] = field(init=False)
    session_cookie_path: Union[str, Path] = field(init=False)
    aoc_tiles_dir: Union[str, Path] = field(init=False)
    image_dir: Union[str, Path] = field(init=False)
    cache_dir: Union[str, Path] = field(init=False)

    verbose: bool = field(default=False, metadata={"help": "Whether to print debug information."})

    what_to_show_on_right_side: Literal["auto", "checkmark", "time_and_rank", "loc"] = field(
        default="auto", metadata={
            "help": "What information to display on the right side of each tile. "
                    "'checkmark' only displays a checkmark for each part if the day is solved. "
                    "'time_and_rank' displays the time and rank on the global leaderboard (requires session.cookie). "
                    "'loc' displays the number of lines of code of the solution (not implemented. "
                    "'auto' will use 'time_and_rank' if session.cookie exists, otherwise 'checkmark'."}
    )
    count_as_solved_when: Literal["auto", "on_leaderboard", "file_exists", "either", "both"] = field(
        default="auto",
        metadata={
            "help": "Condition to count a task as solved. Note that 'on_leaderboard', 'either' and 'both' require a "
                    "session cookie. 'auto' will use 'both' if session.cookie exists, otherwise 'file_exists'."
        },
    )
    language_sorting: List[str] = field(
        default_factory=list,
        metadata={
            "help": "Preferred language extensions order for sorting. For example 'py,rs,js' will make Python "
                    "solutions appear first, then Rust, then JavaScript, then everything else (alphabetically)."
        },
    )
    create_all_days: bool = field(default=False, metadata={"help": "Whether to create entries for all days upfront."})

    auto_add_tiles_to_git: bool = field(default=False, metadata={
        "help": "Whether to automatically add the tile images to git staging."})
    only_use_solutions_in_git: bool = field(default=True, metadata={
        "help": "If true, only solutions will be considered which are tracked by git (git added), "
                "otherwise all solutions will be used. This is useful for example to ignore auto-generated"
                "files, like '.d' in Rust or '.o' files in C++."})

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
    exclude_patterns: List[str] = field(
        default_factory=list, metadata={
            "help": "A list of comma separated glob patterns to ignore when looking for solutions. "
                    "Listing the paths works too. "
                    "For example: '*.py,*.js', '2023/05/05.c' or '2021/**.py'."
                    "Make sure to escape the patterns with single quotes when running from the shell and with"
                    "double quotes when using in the yaml to avoid shell expansion!"
        }
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

    def __post_init__(self):
        self.aoc_dir = Path(self.aoc_dir)

        if not hasattr(self, "readme_path"):
            readmes = [path for path in self.aoc_dir.iterdir() if path.name.lower() == "readme.md"]
            if len(readmes) == 0:
                exit(f"[ERROR] No README.md found in the root directory of the repository '{self.aoc_dir}'.")
            elif len(readmes) > 1:
                exit(f"[ERROR] Multiple README.md files found in the root directory of the repository {readmes}.")
            self.readme_path = readmes[0]

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

        if self.count_as_solved_when == "auto":
            self.count_as_solved_when = "both" if self.session_cookie_path.exists() else "file_exists"

        if self.what_to_show_on_right_side == "auto":
            self.what_to_show_on_right_side = "time_and_rank" if self.session_cookie_path.exists() else "checkmark"

        self.outline_color = ImageColor.getrgb(self.outline_color)
        self.not_completed_color = ImageColor.getrgb(self.not_completed_color)
        self.text_color = ImageColor.getrgb(self.text_color)

        for i, suffix in enumerate(self.language_sorting):
            if not suffix.startswith("."):
                self.language_sorting[i] = "." + suffix

        logger.remove()
        if self.verbose:
            logger.add(sys.stderr, level="DEBUG")

        logger.debug(self)
