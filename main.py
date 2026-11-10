import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

TEXTS = {
    "ru": {
        "welcome": "🎁 Добро пожаловать в Lucky Winner!\n\nСоздавай розыгрыши и выбирай случайных победителей!",
        "giveaway": "🎉 Создание розыгрыша",
        "settings": "⚙️ Настройки",
        "language": "🌍 Выбрать язык",
        "help": "ℹ️ Помощь"
    },
    "en": {
        "welcome": "🎁 Welcome to Lucky Winner!\n\nCreate giveaways and select random winners!",
        "giveaway": "🎉 Create giveaway",
        "settings": "⚙️ Settings",
        "language": "🌍 Select language",
        "help": "ℹ️ Help"
    },
    "de": {
        "welcome": "🎁 Willkommen bei Lucky Winner!\n\nErstelle Gewinnspiele und wähle zufällige Gewinner!",
        "giveaway": "🎉 Gewinnspiel erstellen",
        "settings": "⚙️ Einstellungen",
        "language": "🌍 Sprache wählen",
        "help": "ℹ️ Hilfe"
    }
}

user_languages = {}


def main_menu(lang):
    t = TEXTS[lang]
    keyboard = [
        [InlineKeyboardButton(t["giveaway"], callback_data="giveaway")],
        [InlineKeyboardButton(t["settings"], callback_data="settings")],
        [InlineKeyboardButton(t["language"], callback_data="language")],
        [InlineKeyboardButton(t["help"], callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = user.language_code[:2] if user.language_code else "en"

    if lang not in TEXTS:
        lang = "en"

    user_languages[user.id] = lang

    await update.message.reply_text(
        TEXTS[lang]["welcome"],
        reply_markup=main_menu(lang)
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    lang = user_languages.get(user_id, "en")

    if query.data == "language":
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de")]
        ]
        await query.edit_message_text(
            "🌍 Choose your language:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data.startswith("lang_"):
        lang = query.data.split("_")[1]
        user_languages[user_id] = lang
        await query.edit_message_text(
            TEXTS[lang]["welcome"],
            reply_markup=main_menu(lang)
        )

    elif query.data == "giveaway":
        await query.edit_message_text(
            "🎉 Создание розыгрышей скоро будет доступно!"
        )

    elif query.data == "settings":
        await query.edit_message_text("⚙️ Настройки Lucky Winner")

    elif query.data == "help":
        await query.edit_message_text(
            "ℹ️ Lucky Winner — бот для проведения случайных розыгрышей."
        )


def main():
    if not TOKEN:
        raise RuntimeError("Не задан BOT_TOKEN!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))

    print("Lucky Winner запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
