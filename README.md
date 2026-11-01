# Telegram Caption Bot

Бот принимает фото, накладывает случайную подпись из текстового сборника шрифтом **Lobster** и предлагает опубликовать результат в Telegram-канале.

## Возможности

- получение фото от пользователя
- сохранение оригинала в настраиваемую папку с именем `YYYY-MM-DD_HH:mm_<user_id>.jpg`
- случайная подпись из файла-сборника
- отрисовка подписи шрифтом Lobster
- кнопка «Поделиться» — репост в канал из настроек

## Требования

- Python 3.10+ (для локального запуска на Windows удобнее Docker: в имени файла по ТЗ есть `:`)
- токен бота от [@BotFather](https://t.me/BotFather)
- канал, в котором бот добавлен как администратор с правом публиковать сообщения

## Настройка

Все параметры читаются из переменных окружения:

| Переменная       | Описание                                      |
|------------------|-----------------------------------------------|
| `BOT_TOKEN`      | токен Telegram-бота                           |
| `CHANNEL_ID`     | `@username` канала или числовой id (`-100…`)  |
| `IMAGES_PATH`    | папка для сохранения фото пользователей       |
| `CAPTIONS_FILE`  | путь к текстовому файлу с подписями           |
| `FONT_PATH`      | путь к `Lobster-Regular.ttf` (необязательно)  |

Файл-сборник — обычный текст, **одна фраза на строку**.

Пример:

```bash
cp .env.example .env
# отредактируйте .env и экспортируйте переменные, либо передайте их в Docker
```

В PowerShell:

```powershell
$env:BOT_TOKEN="ваш_токен"
$env:CHANNEL_ID="@your_channel"
$env:IMAGES_PATH="images"
$env:CAPTIONS_FILE="data/captions.txt"
$env:FONT_PATH="fonts/Lobster-Regular.ttf"
```

## Локальный запуск

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Docker

```bash
docker build -t telegram-caption-bot .
docker run --rm \
  -e BOT_TOKEN="ваш_токен" \
  -e CHANNEL_ID="@your_channel" \
  -e IMAGES_PATH="/app/images" \
  -e CAPTIONS_FILE="/app/data/captions.txt" \
  -e FONT_PATH="/app/fonts/Lobster-Regular.ttf" \
  -v "%cd%/images:/app/images" \
  telegram-caption-bot
```

## Тесты

```bash
pytest -q
```

## Структура

```
bot/                 # логика бота
data/captions.txt    # сборник подписей
fonts/               # шрифт Lobster
images/              # сохранённые фото пользователей
tests/               # юнит-тесты
main.py              # точка входа
Dockerfile
requirements.txt
```

## Зависимости

Минимальный набор:

- `python-telegram-bot` — API Telegram
- `Pillow` — отрисовка текста на изображении
- `pytest` — тесты (только для разработки)

Шрифт Lobster (SIL Open Font License) лежит в `fonts/Lobster-Regular.ttf`.
