"""Entry point for the caption Telegram bot."""

from __future__ import annotations

import logging

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, MessageHandler, filters

from bot.config import Config, ConfigError
from bot.handlers import handle_photo, handle_share_callback, help_command, start


def build_application(config: Config) -> Application:
    application = (
        Application.builder()
        .token(config.bot_token)
        .build()
    )
    application.bot_data["config"] = config

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(CallbackQueryHandler(handle_share_callback))
    return application


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=logging.INFO,
    )
    try:
        config = Config.from_env()
    except ConfigError as exc:
        raise SystemExit(str(exc)) from exc

    application = build_application(config)
    logging.getLogger(__name__).info("Bot started")
    application.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == "__main__":
    main()
