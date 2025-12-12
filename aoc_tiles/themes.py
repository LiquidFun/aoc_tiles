"""Theme system for AoC Tiles.

Provides different visual styles for the generated tiles.
"""

from abc import ABC, abstractmethod
from functools import partial
from pathlib import Path
from typing import List, Tuple, Union

from PIL import Image, ImageColor, ImageDraw

from aoc_tiles.colors import color_similarity, darker_color, extension_to_colors
from aoc_tiles.fonts import main_font, secondary_font
from aoc_tiles.leaderboard import DayScores


def format_time(time: str) -> str:
    """Formats time as mm:ss if the time is below 1 hour, otherwise it returns >1h to a max of >24h"""
    time = time.replace("&gt;", ">")
    if ">" in time:
        formatted = time
    else:
        h, m, s = time.split(":")
        formatted = f">{h}h" if int(h) >= 1 else f"{m}:{s}"
    return f"{formatted:>5}"


class Theme(ABC):
    """Base class for tile themes."""

    name: str = "base"

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def draw_tile(
        self,
        day: str,
        languages: List[str],
        day_scores: Union[DayScores, None],
        path: Path,
        stars: int,
    ) -> None:
        """Draw a tile and save it to the given path."""
        pass


class ModernTheme(Theme):
    """The modern theme with colorful diagonal stripes and PaytoneOne font.

    This is the original/default theme for AoC Tiles.
    """

    name = "modern"

    def draw_tile(
        self,
        day: str,
        languages: List[str],
        day_scores: Union[DayScores, None],
        path: Path,
        stars: int,
    ) -> None:
        """Saves a graphic for a given day and year. Returns the path to it."""
        image = self._get_alternating_background(languages, stars == 2)
        drawer = ImageDraw.ImageDraw(image)
        text_kwargs = {"fill": self.config.text_color}

        # Get all colors of the day, check if any one is similar to TEXT_COLOR
        # If yes, add outline
        for language in languages:
            color = ImageColor.getrgb(extension_to_colors()[language])
            if color_similarity(
                color,
                self.config.text_color,
                self.config.contrast_improvement_threshold,
            ):
                if "outline" in self.config.contrast_improvement_type:
                    text_kwargs["stroke_width"] = 1
                    text_kwargs["stroke_fill"] = self.config.outline_color
                if "dark" in self.config.contrast_improvement_type:
                    text_kwargs["fill"] = self.config.not_completed_color
                break

        draw_text = lambda *args, **kwargs: drawer.text(*args, **kwargs, **text_kwargs)
        draw_line = partial(drawer.line, fill=text_kwargs["fill"], width=2)

        # === Left side ===
        draw_text((3, -5), "Day", align="left", font=main_font(20))
        draw_text((1, -10), str(day), align="center", font=main_font(75))

        # Calculate font size based on number of characters, because it might overflow
        lang_as_str = " ".join(languages)
        lang_font_size = max(6, int(18 - max(0, len(lang_as_str) - 8) * 1.3))
        draw_text((0, 74), lang_as_str, align="left", font=secondary_font(lang_font_size))

        # === Right side (P1 & P2) ===
        for part in (1, 2):
            y = 50 if part == 2 else 0
            time = getattr(day_scores, f"time{part}", None)
            rank = getattr(day_scores, f"rank{part}", None)

            color_override = self.config.top100_color if rank and int(rank) <= 100 else self.config.text_color
            text_kwargs["fill"] = color_override

            if stars >= part:
                draw_text((104, -5 + y), f"P{part} ", align="left", font=main_font(25))

                if self.config.what_to_show_on_right_side == "checkmark" or day_scores is None:
                    draw_line((160, 35 + y, 150, 25 + y))
                    draw_line((160, 35 + y, 180, 15 + y))

                elif self.config.what_to_show_on_right_side == "time_and_rank":
                    draw_text((105, 25 + y), "time", align="right", font=secondary_font(10))
                    draw_text(
                        (143, 3 + y),
                        format_time(time),
                        align="right",
                        font=secondary_font(18),
                    )
                    if rank:
                        draw_text(
                            (105, 35 + y),
                            "rank",
                            align="right",
                            font=secondary_font(10),
                        )
                        draw_text(
                            (133, 23 + y),
                            f"{rank:>6}",
                            align="right",
                            font=secondary_font(18),
                        )

                elif self.config.what_to_show_on_right_side == "loc":
                    raise NotImplementedError("loc is not implemented yet")

            else:
                # Draw cross
                draw_line((140, 15 + y, 160, 35 + y))
                draw_line((140, 35 + y, 160, 15 + y))

        if day_scores is None and not languages:
            draw_line((15, 85, 85, 85))

        # === Divider lines ===
        draw_line((100, 5, 100, 95), width=1)
        draw_line((105, 50, 195, 50), width=1)

        image.save(path)

    def _get_alternating_background(self, languages, both_parts_completed=True, *, stripe_width=20):
        colors = [ImageColor.getrgb(extension_to_colors()[language]) for language in languages]
        if len(colors) == 1:
            colors.append(darker_color(colors[0]))
        image = Image.new("RGB", (200, 100), self.config.not_completed_color)

        def fill_with_colors(colors, fill_only_half):
            for x in range(image.width):
                for y in range(image.height):
                    if fill_only_half and x / image.width + y / image.height > 1:
                        continue
                    image.load()[x, y] = colors[((x + y) // stripe_width) % len(colors)]

        fill_with_colors(
            [
                self.config.not_completed_color,
                darker_color(self.config.not_completed_color),
            ],
            False,
        )
        if colors:
            fill_with_colors(colors, not both_parts_completed)
        return image


# Christmas-themed ASCII patterns for tiling background
AOC_ASCII_PATTERNS = [
    # Snowflakes and stars
    [
        " *  .  * ",
        "  \\ | /  ",
        "---*+*---",
        "  / | \\  ",
        " *  .  * ",
    ],
    # Ornaments and garland
    [
        "-o--o--o-",
        " ' '' ' '",
        "-o--o--o-",
    ],
    # Simple stars
    [
        ".  *  . ",
        " *   *  ",
        ".  *  . ",
    ],
]


class AocTheme(Theme):
    """Advent of Code website-inspired theme.

    Features:
    - Monospace font
    - Dark background with language-colored tint
    - ASCII art decorations
    - Retro terminal aesthetic
    """

    name = "aoc"

    # AoC-style colors
    AOC_BG_BASE = (15, 15, 35)  # Dark blue-black like AoC website
    AOC_GREEN = (0, 153, 0)  # AoC solved star green
    AOC_GOLD = (255, 255, 102)  # AoC gold star
    AOC_TEXT_DIM = (68, 68, 68)  # Dimmed text
    AOC_TEXT_BRIGHT = (204, 204, 204)  # Bright text

    def _get_language_color(self, languages: List[str]) -> Tuple[int, int, int]:
        """Get the GitHub language color for the first language."""
        if languages:
            return ImageColor.getrgb(extension_to_colors()[languages[0]])
        return self.AOC_TEXT_DIM

    def _dim_color(self, color: Tuple[int, int, int], factor: float = 0.4) -> Tuple[int, int, int]:
        """Dim a color by blending it toward the background."""
        return (
            int(self.AOC_BG_BASE[0] * (1 - factor) + color[0] * factor),
            int(self.AOC_BG_BASE[1] * (1 - factor) + color[1] * factor),
            int(self.AOC_BG_BASE[2] * (1 - factor) + color[2] * factor),
        )

    def _draw_glowing_text(
        self,
        image: Image.Image,
        pos: Tuple[int, int],
        text: str,
        color: Tuple[int, int, int],
        font,
        glow_size: int = 5,
        glow_alpha: int = 255,
    ):
        """Draw text with a soft glow effect using RGBA compositing."""
        from PIL import ImageFilter

        # Create a transparent layer for the glow
        glow_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        glow_drawer = ImageDraw.ImageDraw(glow_layer)

        # Draw text for the glow multiple times to build up intensity
        glow_color = (*color, glow_alpha)
        for _ in range(12):  # Draw multiple times to increase intensity before blur
            glow_drawer.text(pos, text, fill=glow_color, font=font)

        # Blur the glow layer to create soft glow
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=glow_size))

        # Composite the glow multiple times to intensify it
        image_rgba = image.convert("RGBA")
        for _ in range(3):
            image_rgba = Image.alpha_composite(image_rgba, glow_layer)

        # Draw main text on top (fully opaque)
        text_drawer = ImageDraw.ImageDraw(image_rgba)
        text_drawer.text(pos, text, fill=(*color, 255), font=font)

        # Convert back and paste
        image.paste(image_rgba.convert("RGB"), (0, 0))

    def draw_tile(
        self,
        day: str,
        languages: List[str],
        day_scores: Union[DayScores, None],
        path: Path,
        stars: int,
    ) -> None:
        """Draw an AoC-themed tile."""
        lang_color = self._get_language_color(languages)
        image = self._create_background(languages, lang_color, stars)
        drawer = ImageDraw.ImageDraw(image)

        mono_font = secondary_font  # SourceCodePro is already monospace

        # Star color based on completion
        if stars == 2:
            star_color = self.AOC_GOLD
        elif stars == 1:
            star_color = self.AOC_GREEN
        else:
            star_color = self.AOC_TEXT_DIM

        text_color = self.AOC_TEXT_BRIGHT

        # Draw day number prominently with glow
        day_str = f"Day {int(day):02d}"
        self._draw_glowing_text(image, (10, 5), day_str, text_color, mono_font(22))

        # Draw stars on the right - fixed position for alignment
        star_text = "*" * stars if stars > 0 else "--"
        # Right-align stars at x=190
        star_x = 165 if stars == 2 else 178
        self._draw_glowing_text(
            image,
            (star_x, 5),
            star_text,
            star_color,
            mono_font(22),
            glow_size=5,
            glow_alpha=60,
        )

        # Draw horizontal separator
        drawer.line((5, 35, 195, 35), fill=self.AOC_TEXT_DIM, width=2)

        # Draw language info - use GitHub language color, brighter, with glow
        if languages:
            lang_str = " ".join(lang.lstrip(".") for lang in languages)
            if len(lang_str) > 18:
                lang_str = lang_str[:15] + "..."
            self._draw_glowing_text(image, (8, 38), f"[{lang_str}]", lang_color, mono_font(14))

        # Draw time/rank info or checkmarks
        for part in (1, 2):
            y_offset = 58 if part == 1 else 78
            time = getattr(day_scores, f"time{part}", None)
            rank = getattr(day_scores, f"rank{part}", None)

            part_color = star_color if stars >= part else self.AOC_TEXT_DIM
            part_color = lang_color

            if stars >= part:
                if self.config.what_to_show_on_right_side == "time_and_rank" and day_scores:
                    time_str = format_time(time) if time else "-----"

                    # Highlight top 100
                    rank_color = self.AOC_GOLD if rank and int(rank) <= 100 else part_color

                    self._draw_glowing_text(image, (10, y_offset), f"P{part}:", part_color, mono_font(14))
                    self._draw_glowing_text(image, (45, y_offset), time_str, part_color, mono_font(14))
                    if rank:
                        # Right-align rank to match stars position (end at ~190)
                        rank_str = f"#{rank}"
                        self._draw_glowing_text(
                            image,
                            (124, y_offset),
                            f"{rank_str:>8}",
                            rank_color,
                            mono_font(14),
                        )
                else:
                    # Checkmark style
                    self._draw_glowing_text(image, (10, y_offset), f"P{part}: ", part_color, mono_font(14))
                    self._draw_glowing_text(image, (50, y_offset), "[OK]", self.AOC_GREEN, mono_font(14))
            else:
                drawer.text(
                    (10, y_offset),
                    f"P{part}: ",
                    fill=self.AOC_TEXT_DIM,
                    font=mono_font(14),
                )
                drawer.text((50, y_offset), "[--]", fill=self.AOC_TEXT_DIM, font=mono_font(14))

        image.save(path)

    def _create_background(self, languages: List[str], lang_color: Tuple[int, int, int], stars: int) -> Image.Image:
        """Create a dark background with subtle language-colored tint and ASCII art."""
        image = Image.new("RGB", (200, 100), self.AOC_BG_BASE)

        # Create a subtle gradient/tint based on language color
        pixels = image.load()
        blend = 0.08 if stars > 0 else 0.03
        bg_tinted = (
            int(self.AOC_BG_BASE[0] * (1 - blend) + lang_color[0] * blend),
            int(self.AOC_BG_BASE[1] * (1 - blend) + lang_color[1] * blend),
            int(self.AOC_BG_BASE[2] * (1 - blend) + lang_color[2] * blend),
        )
        for x in range(image.width):
            for y in range(image.height):
                pixels[x, y] = bg_tinted

        # Draw ASCII art in the background using language color
        self._draw_ascii_decoration(image, languages, lang_color)

        return image

    # AoC Christmas light colors (brighter for background)
    XMAS_COLORS = [
        (120, 50, 50),  # Red
        (50, 120, 50),  # Green
        (50, 50, 120),  # Blue
        (120, 120, 50),  # Yellow
    ]

    def _draw_ascii_decoration(self, image: Image.Image, languages: List[str], lang_color: Tuple[int, int, int]):
        """Draw tiling Christmas ASCII pattern with colorful lights."""
        from PIL import ImageFilter

        # Create a separate layer for the ASCII art so we can blur it
        ascii_layer = Image.new("RGB", image.size, self.AOC_BG_BASE)
        drawer = ImageDraw.ImageDraw(ascii_layer)

        # Use a small monospace font for the ASCII pattern
        tiny_font = secondary_font(8)

        # Create a deterministic seed from languages
        lang_str = "".join(sorted(languages)) if languages else "default"
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(lang_str))

        # Pick a pattern based on seed for consistency
        pattern = AOC_ASCII_PATTERNS[seed % len(AOC_ASCII_PATTERNS)]

        # Create a consistent color mapping for each character based on seed
        char_color_map = {}
        all_chars = sorted(set(c for line in pattern for c in line if c != " "))
        for i, char in enumerate(all_chars):
            char_color_map[char] = self.XMAS_COLORS[(seed + ord(char)) % len(self.XMAS_COLORS)]

        # Calculate pattern dimensions
        pattern_height = len(pattern)
        pattern_width = len(pattern[0]) if pattern else 0
        char_width = 5  # Approximate width per character at size 8
        char_height = 10  # Approximate height per line at size 8

        tile_width = pattern_width * char_width
        tile_height = pattern_height * char_height

        # Tile the pattern across the entire background
        for tile_y in range(-tile_height, image.height + tile_height, tile_height):
            for tile_x in range(-tile_width, image.width + tile_width, tile_width):
                for line_idx, line in enumerate(pattern):
                    for char_idx, char in enumerate(line):
                        if char != " ":
                            color = char_color_map[char]
                            drawer.text(
                                (
                                    tile_x + char_idx * char_width,
                                    tile_y + line_idx * char_height,
                                ),
                                char,
                                fill=color,
                                font=tiny_font,
                            )

        # Apply slight blur to the ASCII layer
        ascii_layer = ascii_layer.filter(ImageFilter.GaussianBlur(radius=0.5))

        # Paste the blurred ASCII layer onto the image
        image.paste(ascii_layer, (0, 0))


def get_theme(config) -> Theme:
    themes = {
        "modern": ModernTheme,
        "aoc": AocTheme,
    }

    theme_class = themes.get(config.theme, ModernTheme)
    return theme_class(config)
