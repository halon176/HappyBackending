import os

from dotenv import load_dotenv

load_dotenv()

# la chiave va messa in un file chiamato .env nella stessa directory
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
