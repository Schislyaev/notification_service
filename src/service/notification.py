from functools import lru_cache

from aio_pika import Connection, Message
from aio_pika.abc import AbstractChannel
from aioredis import Redis
from fastapi import Depends

from core.logger import Logger
from db.rabbit import get_rabbit
from db.redis import get_redis
from model.notifications import Event


class NotificationService:

    def __init__(self, connection: Connection, channel: AbstractChannel, redis: Redis):
        self.connection = connection
        self.channel = channel
        self.redis_client = redis
        self.logger = Logger(__name__)

    async def connect_queue(self, channel_name: str = None):
        try:
            await self.channel.declare_queue(channel_name, durable=True)
        except Exception as er:
            self.logger.exception(er)

    async def send_notification(self, event: Event) -> None:
        event_data = event.dict()
        event_id = event_data['event_id']
        if await self.redis_client.setnx(event_id, 1) == 0:
            # Event ID already processed
            return

        try:
            message = Message(body=event.json().encode('utf-8'), delivery_mode=2)
            await self.channel.default_exchange.publish(
                message,
                routing_key='notification',
                mandatory=True,
            )
            self.logger.info(f"Notification sent for event: {event_data['event_type']}")
        except Exception as e:
            # Handle exception and requeue event for processing
            self.logger.exception(f"Error sending notification: {str(e)}")
            await self.redis_client.delete(event_id)


@lru_cache()
def get_notification_service(
        redis: Redis = Depends(get_redis),
        rabbit: tuple[Connection, AbstractChannel] = Depends(get_rabbit)
) -> NotificationService:
    return NotificationService(rabbit[0], rabbit[1], redis)
