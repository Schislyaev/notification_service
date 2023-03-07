from pydantic import BaseModel


class Event(BaseModel):
    event_id: str
    event_type: str
    data: dict
