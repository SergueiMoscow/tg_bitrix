import random

import pytest

from app.repository import create_task, get_tasks_by_user, get_all_tasks
from app.db.engine import AsyncSession
from app.db.models import Task


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_create_task():
    user = 'test_user'
    title = 'test_task'
    async with AsyncSession() as session:
        task = await create_task(session, user, title)
        await session.commit()

    async with AsyncSession() as session:
        created_task = await session.get_one(Task, task.id)
    assert created_task.user == user
    assert created_task.title == title


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_get_tasks_by_user(created_tasks):
    random_user = random.choice(list(created_tasks))
    async with AsyncSession() as session:
        tasks = await get_tasks_by_user(session, random_user)
    assert len(tasks) == len(created_tasks[random_user])
    task_titles = list(map(lambda t: t.title, tasks))
    assert set(task_titles) == set(created_tasks[random_user])


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_get_all_tasks(created_tasks):
    async with AsyncSession() as session:
        tasks = await get_all_tasks(session)
