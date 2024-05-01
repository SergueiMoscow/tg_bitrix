import enum

from sqlalchemy import Column, String, Text, Integer, Enum, DateTime, func

from app.db.db import Base

# from app.db.db import Base

USER_LENGTH = 64
TITLE_LENGTH = 128


class StatusEnum(enum.Enum):
    OPENED = 'открыт'
    IN_WORK = 'в работе'
    SUSPENDED = 'приостановлен'
    WAITING_INFO = 'требуется информация'
    CLOSED = 'закрыт'


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user = Column(String(USER_LENGTH), nullable=False)
    title = Column(String(TITLE_LENGTH), nullable=False)
    body = Column(Text())
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.OPENED)
    created_at = Column(DateTime, server_default=func.now(), index=True)
