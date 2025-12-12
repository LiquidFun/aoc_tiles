"""Animation system for AoC Tiles.

Provides animated GIF output for tiles.
"""

import random
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw

from aoc_tiles.fonts import secondary_font


class Animation:
    """Base class for tile animations."""

    name: str = "base"

    def __init__(self, config):
        self.config = config

    def animate(self, base_image: Image.Image, path: Path) -> None:
        """Create an animated GIF from the base image and save to path."""
        raise NotImplementedError


class SnowAnimation(Animation):
    """Falling snow animation using ASCII characters."""

    name = "snow"

    # Snow characters
    SNOW_CHARS = ["*", ".", "+", "o", "'"]

    # Snow colors (white-ish variations)
    SNOW_COLORS = [
        (255, 255, 255),
        (220, 220, 255),
        (240, 240, 255),
        (200, 200, 220),
    ]

    def __init__(self, config, num_frames: int = 20, num_flakes: int = 25):
        super().__init__(config)
        self.num_frames = num_frames
        self.num_flakes = num_flakes

    def animate(self, base_image: Image.Image, path: Path) -> None:
        """Create a seamlessly looping snow animation GIF."""
        frames = []
        width, height = base_image.size
        loop_height = height + 20  # Total height including off-screen

        # Use path (contains year/day) as seed for consistent but unique snow per tile
        seed = sum(ord(c) * (i + 1) for i, c in enumerate(str(path)))
        random.seed(seed)
        flakes = []
        for _ in range(self.num_flakes):
            flakes.append(self._create_flake(width, loop_height))

        # Generate frames
        for frame_idx in range(self.num_frames):
            frame = base_image.copy()
            drawer = ImageDraw.Draw(frame)

            # Progress through the animation (0.0 to 1.0)
            progress = frame_idx / self.num_frames

            for flake in flakes:
                start_x, start_y, char, color, total_travel, font_size, x_drift = flake
                font = secondary_font(font_size)

                # Current y position (wrapping around loop_height)
                y = (start_y + progress * total_travel) % loop_height - 10

                # X position with slight drift (also wraps)
                x = (start_x + progress * x_drift) % width

                # Draw snowflake
                drawer.text((x, y), char, fill=color, font=font)

            frames.append(frame)

        # Save as GIF
        gif_path = path.with_suffix(".gif")
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=100,  # 100ms per frame
            loop=0,  # Loop forever
            optimize=True,
        )

    def _create_flake(self, width: int, loop_height: int) -> Tuple:
        """Create a snowflake that loops seamlessly.

        Total travel is exactly loop_height so position at frame 0
        equals position at frame N.
        """
        x = random.uniform(0, width)
        y = random.uniform(0, loop_height)
        char = random.choice(self.SNOW_CHARS)
        color = random.choice(self.SNOW_COLORS)
        # Travel exactly one loop_height for seamless wrap
        total_travel = loop_height
        font_size = random.randint(6, 12)
        x_drift = random.uniform(-5, 5)
        return (x, y, char, color, total_travel, font_size, x_drift)


def get_animation(config):
    """Factory function to get the appropriate animation based on config."""
    if config.animation == "none":
        return None

    animations = {
        "snow": SnowAnimation,
    }

    animation_class = animations.get(config.animation)
    if animation_class:
        return animation_class(config)
    return None
