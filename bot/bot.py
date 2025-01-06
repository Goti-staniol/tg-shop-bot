from data.cfg import TOKEN

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from redis.asyncio import Redis


redis = Redis(host='127.0.0.1', port=6379, decode_responses=True)
storage = RedisStorage(redis)

bot = Bot(TOKEN)
dp = Dispatcher()