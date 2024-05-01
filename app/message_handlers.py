from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from .services import get_all_tasks_service, create_task_service

form_router = Router()


class AddTask(StatesGroup):
    waiting_for_task_title = State()
    waiting_for_task_body = State()


@form_router.message(Command("add"))
async def bot_start_add_task_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите имя задачи")
    await state.set_state(AddTask.waiting_for_task_title.state)


@form_router.message(AddTask.waiting_for_task_title)
async def bot_get_task_title_handler(message: types.Message, state: FSMContext):
    # Поместите полученное имя задачи во временное состояние
    await state.update_data(task_title=message.text)
    await message.answer("Введите текст задачи")
    await state.set_state(AddTask.waiting_for_task_body.state)


@form_router.message(AddTask.waiting_for_task_body)
async def bot_get_task_body_handler(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user = message.from_user.username
    title = user_data.get("task_title")
    body = message.text
    await create_task_service(user, title, body)

    await message.answer(f"Задача '{title}' создана.")
    await state.clear()


@form_router.message(Command("tsk"))
async def bot_get_all_task_handler(message: types.Message):
    tasks = await get_all_tasks_service()
    await message.answer(tasks)


@form_router.message()
async def bot_invalid_input(message: types.Message):
    # Если есть такое имя пользователя - отобразить список его задач.
    tasks = await get_all_tasks_service()
    if tasks != '':
        await message.answer(tasks)
    else:
        await message.reply("Неверный ввод...")
