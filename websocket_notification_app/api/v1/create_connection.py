from fastapi import APIRouter, Query, WebSocket
from services.notification_service import get_notification_service

from grpc_src.service.helpers import get_user

router = APIRouter()


@router.websocket_route('/connect')
async def user_connection(websocket: WebSocket, token: str = Query(default='')):
    user_id = await get_user(token, '/connect')
    service = get_notification_service()
    await service.connect(websocket, user_id)

    while websocket.client_state == websocket.client_state.CONNECTED:
        await websocket.receive()

    service.disconnect(user_id)
