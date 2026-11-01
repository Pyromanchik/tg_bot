"""Tests for environment-based configuration."""

from __future__ import annotations

import pytest

from bot.config import Config, ConfigError


def test_config_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BOT_TOKEN", "token")
    monkeypatch.setenv("CHANNEL_ID", "@channel")
    monkeypatch.setenv("IMAGES_PATH", "images")
    monkeypatch.setenv("CAPTIONS_FILE", "data/captions.txt")
    monkeypatch.delenv("FONT_PATH", raising=False)

    config = Config.from_env()

    assert config.bot_token == "token"
    assert config.channel_id == "@channel"
    assert config.images_path == "images"
    assert config.captions_file == "data/captions.txt"
    assert config.font_path.endswith("Lobster-Regular.ttf")


def test_config_requires_bot_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BOT_TOKEN", raising=False)
    monkeypatch.setenv("CHANNEL_ID", "@channel")
    monkeypatch.setenv("IMAGES_PATH", "images")
    monkeypatch.setenv("CAPTIONS_FILE", "data/captions.txt")

    with pytest.raises(ConfigError):
        Config.from_env()
