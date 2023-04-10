from django.shortcuts import get_object_or_404

from bot_app.app import bot, dp
from home_office_drf.main import models

from aiogram import types


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"Привет, {get_object_or_404(models.User, telegram_id=)}")



