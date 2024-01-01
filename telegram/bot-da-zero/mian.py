import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Ciao dal nostro bellissimo bot, {update.message.from_user.first_name}")


def main() -> None:
    application = Application.builder().token("6704403104:AAEcBb6QQWVwYa0GTrYhp14DvLC-r6B-el8").build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == "__main__":
    main()
