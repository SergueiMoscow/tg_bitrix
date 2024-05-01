from .repository import create_task, get_all_tasks, get_tasks_by_user
from app.db.engine import AsyncSession


async def create_task_service(user, title, body):
    async with AsyncSession() as session:
        await create_task(session, user, title, body)
        await session.commit()


async def get_all_tasks_service(user: str | None = None) -> str:
    async with AsyncSession() as session:
        if user is not None:
            tasks = await get_tasks_by_user(session, user)
        else:
            tasks = await get_all_tasks(session)
    result = ''
    for task in tasks:
        result += (
            f'<b>=== {task.title} ===</b>\n'
            f'{task.body}\n'
            f'<i>{task.created_at.strftime("%d.%m.%Y %H:%M")} ({task.user})</i>\n'
            f'{"-" * 10}\n'
        )
    return result
