# app/bot.py
import os
from dotenv import load_dotenv
from infra.config import get_settings

load_dotenv()
from app.discord_handlers import client

client.run(os.environ["DISCORD_TOKEN"])
