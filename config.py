import os

from dotenv import load_dotenv

load_dotenv()

API_KEY_WEATHER = os.getenv('API_KEY_WEATHER')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DEV_ID = os.getenv('DEV_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
BOT_NAME = os.getenv('BOT_NAME')
CHANNEL_LINK = os.getenv('CHANNEL_LINK')