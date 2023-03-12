from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Header, Query, Request

from grpc_src.service.helpers import jwt_check
from model.stored_note import (Note, NoteCRUD, StoredNote,
                               get_stored_note_service)
from service.auth_service import JWTBearer

router = APIRouter()
bearer = JWTBearer()


@router.get(
    path='/notes/{user_id}',
    summary='Получить события нотификации',
    description='Получить данные по событиям нотификации для пользователя',
    response_description='Вывод данных по имеющимся событиям нотификации',
    response_model=list[StoredNote],
    dependencies=[Depends(JWTBearer())]
)
async def get_notes_by_id(
        request: Request,
        service: NoteCRUD = Depends(get_stored_note_service),
        authorization: str = Header(default=None),
        user_id: UUID = Query(default=None)
) -> list[StoredNote]:

    _ = await jwt_check(token=authorization, request_path=request.url)

    notes = await service.get_all_by_user_id(user_id=user_id)

    return [StoredNote(**note.dict()) for note in notes]


@router.get(
    path='/notes',
    summary='Получить события нотификации по токену',
    description='Получить данные по событиям нотификации для пользователя по токену',
    response_description='Вывод данных по имеющимся событиям нотификации',
    response_model=list[StoredNote],
    dependencies=[Depends(JWTBearer())]
)
async def get_notes_by_token(
        request: Request,
        service: NoteCRUD = Depends(get_stored_note_service),
        authorization: str = Header(default=None),
) -> list[StoredNote]:

    id_accepted = await jwt_check(token=authorization, request_path=request.url)

    notes = await service.get_all_by_user_id(user_id=UUID(id_accepted))

    return [StoredNote(**note.dict()) for note in notes]


@router.post(
    path='/notes',
    summary='Сохранить события нотификации',
    description='Сохранить данные по событиям нотификации',
    response_description='Сохраненные данные по имеющимся событиям нотификации',
    response_model=StoredNote,
    dependencies=[Depends(JWTBearer())]
)
async def post_note(
        service: NoteCRUD = Depends(get_stored_note_service),
        authorization: str = Header(default=None),
        note: Note = Body(...)
) -> StoredNote | None:

    if not bearer.verify_jwt(authorization):
        return None

    note.time_posted = datetime.utcnow()    # Нужно ли фиксировать время здесь или в воркере?
    stored_note = await service.store_note(note=note)

    return StoredNote(**stored_note.dict())
