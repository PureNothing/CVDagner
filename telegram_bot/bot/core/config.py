from dotenv import load_dotenv
from aiogram import Bot
import os
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GRAPHQL_URL = "http://localhost:8001/graphql"
AI_THRESHOLD_URL = "http://localhost/ai_rules_message"
KAFKA_URL = "localhost:9092"
SETTINGS_KEY = os.getenv("SETTINGS_KEY")
BUDDY_ID = os.getenv("BUDDY_ID")
OWNER_ID = os.getenv("OWNER_ID")

bot = Bot(token=BOT_TOKEN)
