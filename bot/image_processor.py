"""Save photos and draw captions with the Lobster font."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def make_image_filename(user_id: int, when: datetime | None = None) -> str:
    """Build filename: YYYY-MM-DD_HH:mm_<user id>.jpg"""
    moment = when or datetime.now()
    return f"{moment.strftime('%Y-%m-%d_%H:%M')}_{user_id}.jpg"


def save_user_image(data: bytes, images_path: str | Path, user_id: int) -> Path:
    """Save original user photo and return the saved path."""
    directory = Path(images_path)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / make_image_filename(user_id)
    path.write_bytes(data)
    return path


def _fit_font(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_path: str | Path,
    max_width: int,
    max_size: int = 72,
    min_size: int = 16,
) -> ImageFont.FreeTypeFont:
    """Pick the largest Lobster size that fits within max_width."""
    size = max_size
    while size >= min_size:
        font = ImageFont.truetype(str(font_path), size=size)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(str(font_path), size=min_size)


def draw_caption(
    image_data: bytes,
    caption: str,
    font_path: str | Path,
) -> bytes:
    """Draw caption at the bottom of the image and return JPEG bytes."""
    with Image.open(BytesIO(image_data)) as image:
        image = image.convert("RGB")
        draw = ImageDraw.Draw(image)

        margin = max(20, image.width // 40)
        max_width = image.width - 2 * margin
        font = _fit_font(draw, caption, font_path, max_width)

        bbox = draw.textbbox((0, 0), caption, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (image.width - text_width) // 2
        y = image.height - text_height - margin

        # Dark outline for readability on any background
        outline = max(2, font.size // 18)
        for dx in range(-outline, outline + 1):
            for dy in range(-outline, outline + 1):
                if dx or dy:
                    draw.text((x + dx, y + dy), caption, font=font, fill="black")
        draw.text((x, y), caption, font=font, fill="white")

        output = BytesIO()
        image.save(output, format="JPEG", quality=92)
        return output.getvalue()
