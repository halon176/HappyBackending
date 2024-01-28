import logging

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from telegram import Update

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Ciao dal nostro bellissimo bot, {update.message.from_user.first_name}")


async def hanle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open(f"chats/{update.message.chat_id}.log", "a") as file:
        file.write(f"{update.message.from_user.id} - {update.message.text}\n")

    await update.message.reply_text(f"Ciao a {update.message.from_user.first_name}")


def main() -> None:
    application = Application.builder().token("6704403104:AAFH0RU77qjefwCTOygOINroka7J9SjVvcg").build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.Regex(r"(?i)ciao"), hanle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
