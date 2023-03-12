from dataclasses import dataclass, field

from fastapi import WebSocket

from api.v1.schemas import Notification


@dataclass
class NotificationService:
    sockets: dict[str, WebSocket] = field(default_factory=dict)

    async def connect(self, socket: WebSocket, user_id: str) -> None:
        await socket.accept()
        self.sockets[user_id] = socket

    def disconnect(self, user_id: str) -> None:
        self.sockets.pop(user_id, None)

    async def send(self, notification: Notification) -> None:
        socket = self.sockets.get(str(notification.user_uuid), None)
        if socket:
            await socket.send_text(notification.text)


service = NotificationService()


def get_notification_service():
    return service
