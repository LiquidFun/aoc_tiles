import math
from functools import partial
from pathlib import Path
from typing import List, Tuple, Union, Dict

from PIL import ImageColor, Image
from PIL.ImageDraw import ImageDraw

from aoc_tiles.colors import color_similarity, darker_color, extension_to_colors
from aoc_tiles.config import Config
from aoc_tiles.fonts import main_font, secondary_font
from aoc_tiles.leaderboard import DayScores


def format_time(time: str) -> str:
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


class TileDrawer:
    def __init__(self, config: Config):
        self.config = config

    def draw_tile(
        self, day: str, languages: List[str], day_scores: Union[DayScores, None], path: Path, is_solved: bool
    ):
        """Saves a graphic for a given day and year. Returns the path to it."""
        image = self.get_alternating_background(languages, is_solved)
        drawer = ImageDraw(image)
        text_kwargs = {"fill": self.config.text_color}

        # Get all colors of the day, check if any one is similar to TEXT_COLOR
        # If yes, add outline
        for language in languages:
            color = ImageColor.getrgb(extension_to_colors()[language])
            if color_similarity(color, self.config.text_color, self.config.contrast_improvement_threshold):
                if "outline" in self.config.contrast_improvement_type:
                    text_kwargs["stroke_width"] = 1
                    text_kwargs["stroke_fill"] = self.config.outline_color
                if "dark" in self.config.contrast_improvement_type:
                    text_kwargs["fill"] = self.config.not_completed_color
                break

        draw_text = partial(drawer.text, **text_kwargs)
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

            if is_solved:
                draw_text((104, -5 + y), f"P{part} ", align="left", font=main_font(25))

                if self.config.what_to_show_on_right_side == "checkmark":
                    draw_line((160, 35 + y, 150, 25 + y))
                    draw_line((160, 35 + y, 180, 15 + y))

                if self.config.what_to_show_on_right_side == "time_and_rank":
                    draw_text((105, 25 + y), "time", align="right", font=secondary_font(10))
                    draw_text((105, 35 + y), "rank", align="right", font=secondary_font(10))
                    draw_text((143, 3 + y), format_time(time), align="right", font=secondary_font(18))
                    draw_text((133, 23 + y), f"{rank:>6}", align="right", font=secondary_font(18))

                if self.config.what_to_show_on_right_side == "loc":
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

    def get_alternating_background(self, languages, both_parts_completed=True, *, stripe_width=20):
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

        fill_with_colors([self.config.not_completed_color, darker_color(self.config.not_completed_color)], False)
        if colors:
            fill_with_colors(colors, not both_parts_completed)
        return image

    def draw_star(self, drawer: ImageDraw, at: Tuple[int, int], size=9, color="#ffff0022", num_points=5):
        """Draws a star at the given position"""
        diff = math.pi * 2 / num_points / 2
        points: List[Tuple[float, float]] = []
        for angle in [diff * i - math.pi / 2 for i in range(num_points * 2)]:
            factor = size if len(points) % 2 == 0 else size * 0.4
            points.append((at[0] + math.cos(angle) * factor, at[1] + math.sin(angle) * factor))
        drawer.polygon(points, fill=color)
