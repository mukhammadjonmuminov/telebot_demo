import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from database import Database

API_TOKEN = os.getenv('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await Database.create_table()
    user_id = message.from_user.id
    username = message.from_user.username
    if await Database.check_user(user_id):
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "chat_id": user_id
        }
        await Database.save_user(data)
        await message.reply(f'Salom @{username}')
    else:
        await message.reply(f"Sizni yana ko'rganimdan xursandaman @{username}")



@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)