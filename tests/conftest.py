import pytest
from alembic import command
from alembic.config import Config

from app.settings import settings, ROOT_DIR
from app.db.engine import Session
from sqlalchemy import text as sa_text

from app.db.models import Task


@pytest.fixture
def apply_migrations():
    assert 'TEST' in settings.DATABASE_SCHEMA.upper(), 'Попытка использовать не тестовую схему.'

    alembic_cfg = Config(str(ROOT_DIR / 'alembic.ini'))
    alembic_cfg.set_main_option('script_location', str(ROOT_DIR / 'alembic'))
    command.downgrade(alembic_cfg, 'base')
    command.upgrade(alembic_cfg, 'head')

    yield command, alembic_cfg

    command.downgrade(alembic_cfg, 'base')

    with Session() as session:
        session.execute(sa_text(f'DROP SCHEMA IF EXISTS {settings.DATABASE_SCHEMA} CASCADE;'))
        session.commit()


@pytest.fixture
def created_tasks(faker):
    count_users = faker.random_int(2, 5)
    users = {}
    with Session() as session:
        for count_user in range(count_users):
            user: str = faker.name()
            count_tasks = faker.random_int(2, 5)
            user_tasks = []
            for count_task in range(count_tasks):
                title = faker.sentence()
                task = Task(
                    user=user,
                    title=title
                )
                session.add(task)
                user_tasks.append(title)
            users[user] = user_tasks
        session.commit()
    return users
