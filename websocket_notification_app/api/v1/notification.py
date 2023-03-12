from fastapi import APIRouter, Body, Depends, Request, Response
from services.notification_service import (NotificationService,
                                           get_notification_service)

from api.v1.schemas import Notification

router = APIRouter()


@router.post('/notification')
async def send_notification(
    request: Request,
    notification: Notification = Body(...),
    service: NotificationService = Depends(get_notification_service)
) -> Response:
    await service.send(notification)
    return Response(status_code=200)
