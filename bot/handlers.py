"""Telegram update handlers."""

from __future__ import annotations

import logging
from io import BytesIO

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.captions import load_captions, pick_random_caption
from bot.config import Config
from bot.image_processor import draw_caption, save_user_image

logger = logging.getLogger(__name__)

SHARE_CALLBACK = "share_yes"
DECLINE_CALLBACK = "share_no"


def share_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Поделиться", callback_data=SHARE_CALLBACK),
                InlineKeyboardButton("Не сейчас", callback_data=DECLINE_CALLBACK),
            ]
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "Пришлите фото — я добавлю случайную подпись и предложу поделиться ею."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None:
        return
    await update.message.reply_text(
        "Отправьте изображение. Бот сохранит его, наложит подпись шрифтом Lobster "
        "и спросит, можно ли опубликовать результат в канале."
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message is None or not update.message.photo or update.effective_user is None:
        return

    config: Config = context.application.bot_data["config"]
    user_id = update.effective_user.id
    photo = update.message.photo[-1]

    try:
        file = await context.bot.get_file(photo.file_id)
        buffer = BytesIO()
        await file.download_to_memory(buffer)
        image_data = buffer.getvalue()

        save_user_image(image_data, config.images_path, user_id)

        captions = load_captions(config.captions_file)
        caption = pick_random_caption(captions)
        result = draw_caption(image_data, caption, config.font_path)

        sent = await update.message.reply_photo(
            photo=result,
            caption=f"Подпись: {caption}\nПоделиться картинкой в канале?",
            reply_markup=share_keyboard(),
        )
        context.user_data["last_result_file_id"] = sent.photo[-1].file_id
        context.user_data["last_caption"] = caption
    except Exception:
        logger.exception("Failed to process photo from user %s", user_id)
        await update.message.reply_text(
            "Не удалось обработать фото. Попробуйте ещё раз или другое изображение."
        )


async def handle_share_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query
    if query is None:
        return

    await query.answer()
    config: Config = context.application.bot_data["config"]

    if query.data == DECLINE_CALLBACK:
        await query.edit_message_reply_markup(reply_markup=None)
        if query.message is not None:
            await query.message.reply_text("Хорошо, никому не покажу.")
        return

    if query.data != SHARE_CALLBACK:
        return

    file_id = context.user_data.get("last_result_file_id")
    caption = context.user_data.get("last_caption", "")
    if not file_id:
        if query.message is not None:
            await query.message.reply_text(
                "Не нашёл картинку для публикации. Пришлите новое фото."
            )
        return

    try:
        await context.bot.send_photo(
            chat_id=config.channel_id,
            photo=file_id,
            caption=caption,
        )
        await query.edit_message_reply_markup(reply_markup=None)
        if query.message is not None:
            await query.message.reply_text("Готово! Картинка опубликована в канале.")
    except Exception:
        logger.exception("Failed to share photo to channel %s", config.channel_id)
        if query.message is not None:
            await query.message.reply_text(
                "Не удалось опубликовать в канале. Проверьте, что бот — админ канала."
            )
