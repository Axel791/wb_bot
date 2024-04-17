from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.core.config import settings

bot = Bot(settings.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()
