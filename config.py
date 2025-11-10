from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT") or ""
WEATHER_API_KEY = getenv("WEATHER_API_KEY") or ""


if not BOT_TOKEN:
    raise ValueError(" BOT_TOKEN not found in .env file")

if not WEATHER_API_KEY:
    raise ValueError(" WEATHER_API_KEY not found in .env file")

print("Configuration loaded")
