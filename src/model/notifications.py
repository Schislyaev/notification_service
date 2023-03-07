from datetime import datetime, timedelta
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

    event_type: Literal['ugc', 'periodic']  # Пока ограничился двумя видами сценария
    event_tz: str   # Таймзона
    data: str   # Тело сообщения. Возможно будет переработана в словарь для темплейтов

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
    request_id: str = Field(...)    # Поле прилетающее из nginx
    time_created: datetime = Field(default_factory=datetime.utcnow)
    time_posted: datetime = Field(default=None)
    event: Event

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


#############################################################
# Ниже заготовки для ручек посылающих в RabbitMQ
#############################################################


class PeriodicNote(BaseNote):
    start: datetime = datetime.now()
    stop: datetime | None = None
    period: timedelta

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = 'events'
        use_revision = False


class UGCNote(BaseNote):
    pass

    class Config:
        arbitrary_types_allowed = True

    class Settings:
        name = 'events'
        use_revision = False
