import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import BotCommand

from app.settings import settings
from app.message_handlers import form_router

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
dp = Dispatcher()

INSTRUCTION = '/add - добавить задачу\n/tsk - вывести список задач'


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/add', description='Создать задачу'),
        BotCommand(command='/tsk', description='Список задач'),
        ]
    await bot.set_my_commands(main_menu_commands)


@dp.message(CommandStart())
async def start(message: types.Message):
    """Returns start and help text"""
    await message.answer(f'Привет, {message.from_user.username}!\n{INSTRUCTION}')


async def main():
    bot = Bot(settings.TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.startup.register(set_main_menu)
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
