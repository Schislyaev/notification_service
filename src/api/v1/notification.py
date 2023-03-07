from fastapi import APIRouter, Body, Depends, Header, Request

from model.notifications import Event
from service.auth_service import JWTBearer
from service.notification import NotificationService, get_notification_service

router = APIRouter()


@router.post('/ugc_note', dependencies=[Depends(JWTBearer())])
async def get_ugc_note(
        request: Request,
        service: NotificationService = Depends(get_notification_service),
        event: Event = Body(...),
        # Другие микросервисы запаковывают в Header токен зашифрованный в соответствии с секретным ключом,
        # известным обоим сервисам. В режиме дебага принимается любой токен
        authorization=Header(default=None),
):
    if not JWTBearer.verify_jwt(authorization):
        return
    ...


@router.post('/get_periodic_note', dependencies=[Depends(JWTBearer())])
async def get_periodic_note(
        request: Request,
        service: NotificationService = Depends(get_notification_service),
        event: Event = Body(...),
        authorization=Header(default=None),
):
    if not JWTBearer.verify_jwt(authorization):
        return
    ...


@router.post('/hand_made_note', dependencies=[Depends(JWTBearer())])
async def get_hand_made_note(
        request: Request,
        service: NotificationService = Depends(get_notification_service),
        event: Event = Body(...),
        authorization=Header(default=None),
):
    if not JWTBearer.verify_jwt(authorization):
        return
    ...
