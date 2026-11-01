"""Load bot settings from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass


class ConfigError(ValueError):
    """Raised when a required environment variable is missing or invalid."""


def _require(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ConfigError(f"Environment variable {name} is required")
    return value


@dataclass(frozen=True)
class Config:
    bot_token: str
    channel_id: str
    images_path: str
    captions_file: str
    font_path: str

    @classmethod
    def from_env(cls) -> Config:
        return cls(
            bot_token=_require("BOT_TOKEN"),
            channel_id=_require("CHANNEL_ID"),
            images_path=_require("IMAGES_PATH"),
            captions_file=_require("CAPTIONS_FILE"),
            font_path=os.environ.get(
                "FONT_PATH",
                os.path.join("fonts", "Lobster-Regular.ttf"),
            ),
        )
