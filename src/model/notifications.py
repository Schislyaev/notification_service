from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class Event(BaseModel):
    """
    Общая модель события, которое подлежит отправке в очередь.
    """

    event_type: Literal['ugc', 'periodic', 'custom']  # Пока ограничился двумя видами сценария
    broadcast_type: list[Literal['sms', 'email', 'ws']]
    event_tz: str   # Таймзона
    data: str   # !!Done -  Переработана в модель для темплейтов

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class BaseNote(BaseModel):
    """
    Базовая модель нотификации, включающей событие.

    Нотификация - сущность обладающая атрибутами для отправки
    """
    id: UUID = Field(default_factory=uuid4, alias="_id")
    user_id: UUID
    request_id: str = Field(default=None)    # Поле прилетающее из nginx (default=None пока дебаг)
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_posted: datetime = Field(default=None)
    event: Event

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        orm_mode = True


class BaseNoteIn(BaseModel):
    """
    Модель на вход в ручку.
    """
    user_id: UUID
    event: Event

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        orm_mode = True
