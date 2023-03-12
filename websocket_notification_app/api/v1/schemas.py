import uuid

from pydantic import BaseModel


class Notification(BaseModel):
    user_uuid: uuid.UUID
    text: str
