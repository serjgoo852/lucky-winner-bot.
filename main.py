import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# The token is supplied by the hosting platform as an environment variable.
# Never paste the real token into this file or commit it to GitHub.
TOKEN = os.getenv("BOT_TOKEN", "").strip()

TEXTS = {
    "ru": {
        "welcome": "🎁 Добро пожаловать в Lucky Winner!\n\nСоздавай розыгрыши и выбирай случайных победителей!",
        "giveaway": "🎉 Создать розыгрыш",
        "settings": "⚙️ Настройки",
        "language": "🌍 Выбрать язык",
        "help": "ℹ️ Помощь",
        "soon": "🎉 Создание розыгрышей скоро будет доступно!",
        "settings_text": "⚙️ Настройки Lucky Winner",
        "help_text": "ℹ️ Lucky Winner — бот для проведения розыгрышей и случайного выбора победителей.",
        "choose_language": "🌍 Выбери язык:",
        "language_saved": "✅ Язык изменён.",
    },
    "en": {
        "welcome": "🎁 Welcome to Lucky Winner!\n\nCreate giveaways and choose random winners!",
        "giveaway": "🎉 Create giveaway",
        "settings": "⚙️ Settings",
        "language": "🌍 Choose language",
        "help": "ℹ️ Help",
        "soon": "🎉 Giveaway creation will be available soon!",
        "settings_text": "⚙️ Lucky Winner settings",
        "help_text": "ℹ️ Lucky Winner is a bot for running giveaways and choosing random winners.",
        "choose_language": "🌍 Choose your language:",
        "language_saved": "✅ Language changed.",
    },
    "de": {
        "welcome": "🎁 Willkommen bei Lucky Winner!\n\nErstelle Gewinnspiele und wähle zufällige Gewinner!",
        "giveaway": "🎉 Gewinnspiel erstellen",
        "settings": "⚙️ Einstellungen",
        "language": "🌍 Sprache wählen",
        "help": "ℹ️ Hilfe",
        "soon": "🎉 Die Erstellung von Gewinnspielen ist bald verfügbar!",
        "settings_text": "⚙️ Lucky Winner Einstellungen",
        "help_text": "ℹ️ Lucky Winner ist ein Bot für Gewinnspiele und die zufällige Auswahl von Gewinnern.",
        "choose_language": "🌍 Wähle deine Sprache:",
        "language_saved": "✅ Sprache geändert.",
    },
}


def get_language(context: ContextTypes.DEFAULT_TYPE, telegram_language: str | None = None) -> str:
    """Return the saved language or detect it from Telegram."""
    saved = context.user_data.get("language")
    if saved in TEXTS:
        return saved

    detected = (telegram_language or "en")[:2].lower()
    return detected if detected in TEXTS else "en"


def main_menu(language: str) -> InlineKeyboardMarkup:
    labels = TEXTS[language]
    keyboard = [
        [InlineKeyboardButton(labels["giveaway"], callback_data="giveaway")],
        [InlineKeyboardButton(labels["settings"], callback_data="settings")],
        [InlineKeyboardButton(labels["language"], callback_data="language")],
        [InlineKeyboardButton(labels["help"], callback_data="help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def language_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.effective_message
    if message is None:
        return

    language = get_language(context, user.language_code if user else None)
    await message.reply_text(
        TEXTS[language]["welcome"],
        reply_markup=main_menu(language),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = update.effective_message
    if message is None:
        return

    language = get_language(context, user.language_code if user else None)
    await message.reply_text(TEXTS[language]["help_text"])


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return

    await query.answer()
    data = query.data or ""
    language = get_language(context, query.from_user.language_code)

    if data == "language":
        await query.edit_message_text(
            TEXTS[language]["choose_language"],
            reply_markup=language_menu(),
        )
        return

    if data.startswith("lang_"):
        selected = data.removeprefix("lang_")
        if selected not in TEXTS:
            await query.answer("Unknown language", show_alert=True)
            return

        context.user_data["language"] = selected
        await query.edit_message_text(
            TEXTS[selected]["language_saved"] + "\n\n" + TEXTS[selected]["welcome"],
            reply_markup=main_menu(selected),
        )
        return

    if data == "back":
        await query.edit_message_text(
            TEXTS[language]["welcome"],
            reply_markup=main_menu(language),
        )
    elif data == "giveaway":
        await query.edit_message_text(TEXTS[language]["soon"])
    elif data == "settings":
        await query.edit_message_text(TEXTS[language]["settings_text"])
    elif data == "help":
        await query.edit_message_text(TEXTS[language]["help_text"])


def main() -> None:
    if not TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not set. Add the token in your hosting platform's "
            "environment variables; do not put it in main.py."
        )

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(handle_buttons))

    logger.info("Lucky Winner bot is starting...")
    application.run_polling()


if __name__ == "__main__":
    main()
