from typing import List

from sqlalchemy import select

from .settings import settings
from .db.models import Task
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionType


async def create_task(
    session: AsyncSessionType,
    user: str,
    task_title: str,
    task_body: str = '',
) -> Task:
    task = Task(
        user=user,
        title=task_title,
        body=task_body,
    )
    session.add(task)
    return task


async def get_tasks_by_user(session: AsyncSessionType, user: str) -> List[Task]:
    query = (
        select(Task).
        where(Task.user == user).
        order_by(Task.created_at).
        limit(settings.MAX_COUNT)
    )
    tasks = list(await session.scalars(query))
    return tasks


async def get_all_tasks(session: AsyncSessionType) -> List[Task]:
    query = select(Task).order_by(Task.created_at).limit(settings.MAX_COUNT)
    tasks = list(await session.scalars(query))
    return tasks
