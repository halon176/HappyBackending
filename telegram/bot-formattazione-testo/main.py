import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def mk2_formatter(text: str) -> str:
    symbols: list = [">", "#", "+", "-", "=", "{", "}", ".", "!"]
    for symbol in symbols:
        index = text.find(symbol)
        while index != -1:
            if index > 0 and text[index - 1] != "\\":
                text = text[:index] + "\\" + text[index:]
            index = text.find(symbol, index + 2)
    return text


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = ("*Il nostro* _bellissimo_ __messaggio__ = `formattato` ~come se fosse~ un  ||arlecchino||"
           "```python\nprint('Hello World')\n```"
           "[LVI](https://th.bing.com/th/id/OIP.z_Kk82irrHEtIIEhn_tTKAHaLH?rs=1&pid=ImgDetMain)")
    await update.message.reply_text(mk2_formatter(msg), parse_mode=ParseMode.MARKDOWN_V2)


async def hanle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open(f"chats/{update.message.chat_id}.log", "a") as file:
        file.write(f"{update.message.from_user.id} - {update.message.text}\n")

    await update.message.reply_text(f"Ciao a {update.message.from_user.first_name}")


def main() -> None:
    application = Application.builder().token("6704403104:AAEuMlC7xlD40FHWhdsS_jYocyTfy0gKbLE").build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.Regex(r"(?i)ciao"), hanle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
