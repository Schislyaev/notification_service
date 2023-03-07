"""
Модель для хранения события нотификации и класс взаимодействия с ней.
"""

from functools import lru_cache
from uuid import UUID

from beanie import Document, exceptions
from pydantic import EmailStr

from core.logger import Logger
from model.notifications import BaseNote


class StoredNote(BaseNote):
    """ Response model """
    user_id: UUID
    email: EmailStr


class Note(Document, BaseNote):
    """ Beanie модель - для взаимодействия с круд. Ее не отдать через resp model"""
    user_id: UUID
    email: EmailStr

    class Settings:
        name = 'events'
        use_revision = False


class NoteCRUD:
    def __init__(self):
        self.logger = Logger(__name__)

    async def store_note(self, note: Note) -> Note:
        try:
            await note.insert()
            return note
        except exceptions.DocumentAlreadyCreated as er:
            self.logger.exception(er)
            raise er

    async def get_all_by_user_id(self, user_id: UUID) -> list:
        try:
            notes = await Note.find(Note.user_id == user_id).to_list()
            return notes
        except exceptions.DocumentNotFound as er:
            self.logger.exception(er)
            raise er


@lru_cache()
def get_stored_note_service() -> NoteCRUD:
    return NoteCRUD()
