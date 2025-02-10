from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import DefaultBotProperties
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import Config, load_config
config: Config = load_config()

bot: Bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(bot=bot, storage=MemoryStorage())
ADMIN_ID = 97185772
