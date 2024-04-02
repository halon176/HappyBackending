import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler,
)

from config import TELEGRAM_BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def callback(update: Update, context: CallbackContext) -> None:
    opzione = update.callback_query.data
    await update.effective_user.send_message(
        f"Benvenut{'o' if opzione == 'maschio' else 'a'} {update.effective_user.username}!"
    )
    await update.callback_query.message.delete()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tastiera = [
        [
            InlineKeyboardButton("Maschio", callback_data="maschio"),
            InlineKeyboardButton("Femmina", callback_data="femmina"),
        ]
    ]
    tastiera_markup = InlineKeyboardMarkup(tastiera)
    await update.message.reply_text("Che genere sei?", reply_markup=tastiera_markup)


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(CallbackQueryHandler(callback))

    application.run_polling()


if __name__ == "__main__":
    main()
