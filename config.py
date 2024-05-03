import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN_LOT')
BOT_NAME = os.getenv('BOT_NAME_LOT')
DEV_ID = int(os.getenv('DEV_ID'))
ADMIN_ID = int(os.getenv('ADMIN_ID'))
CHANNEL_ID = os.getenv('CHANNEL_ID')
CHANNEL_LINK = os.getenv('CHANNEL_LINK')
BASE_USERS = os.getenv('BASE_USERS')
BASE_LOT = os.getenv('BASE_LOT')
