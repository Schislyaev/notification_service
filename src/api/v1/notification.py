from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import APIRouter, Body, Depends, Header, HTTPException, status
from fastapi.responses import JSONResponse

from core.logger import Logger
from model.notifications import BaseNote, BaseNoteIn
from scheduler.scheduler import get_scheduler
from service.auth_service import JWTBearer
from service.cron_service import validate_cron
from service.notification import NotificationService, get_notification_service

router = APIRouter()
bearer = JWTBearer()
logger = Logger(__name__)


@router.post('/post_note', dependencies=[Depends(JWTBearer())])
async def get_ugc_note(
        service: NotificationService = Depends(get_notification_service),
        x_request_id: str = Header(...),
        event: BaseNoteIn = Body(...),
        # Другие микросервисы запаковывают в Header токен зашифрованный в соответствии с секретным ключом,
        # известным обоим сервисам. В режиме дебага принимается любой токен
        authorization=Header(default=None),
):
    if not bearer.verify_jwt(jwtoken=authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    result = await service.send_validated_notification(
        BaseNote(
            request_id=x_request_id,
            **event.dict()
        )
    )

    return result


@router.post('/post_periodic_note', dependencies=[Depends(JWTBearer())])
async def post_periodic_note(
        service: NotificationService = Depends(get_notification_service),
        scheduler: AsyncIOScheduler = Depends(get_scheduler),
        authorization=Header(default=None),
        x_request_id: str = Header(...),
        event: BaseNoteIn = Body(...),
        schedule: dict = Body(...),     # Расписание в формате cron
):

    if not bearer.verify_jwt(authorization):    # Межсервисная авторизация (не надежная)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if not validate_cron(schedule=schedule):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cron schedule error'
        )

    event_out = BaseNote(
        request_id=x_request_id,
        **event.dict(),
    )

    try:
        scheduler.add_job(
            service.send_validated_notification,
            args=[event_out],
            trigger='cron',
            **schedule,
            max_instances=10,
        )
    except Exception as er:
        logger.exception(er)
        raise er

    return JSONResponse(
        status_code=status.HTTP_202_ACCEPTED,
        content={'message': 'Event scheduled successfully'}
    )
