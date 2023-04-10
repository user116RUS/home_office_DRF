import os

from aiogram import Bot, Dispatcher

from . local_settings import API_TOKEN

bot = Bot(API_TOKEN)
dp = Dispatcher(bot)
