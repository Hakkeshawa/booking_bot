import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ORGANIZER_CHAT_ID = os.getenv("ORGANIZER_CHAT_ID")