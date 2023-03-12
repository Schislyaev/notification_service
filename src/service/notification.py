from functools import lru_cache

from aio_pika import Connection, ExchangeType, Message
from aio_pika.abc import AbstractChannel
from aioredis import Redis
from fastapi import Depends

from core.logger import Logger
from core.settings import settings
from db.rabbit import get_rabbit
from db.redis import get_redis
from model.notifications import BaseNote
from service.template_service import validate_template


class NotificationService:

    def __init__(self, connection: Connection, channel: AbstractChannel, redis: Redis):
        self.connection = connection
        self.channel = channel

        self.broadcast: set = set()

        self.redis_client = redis
        self.logger = Logger(__name__)

    async def connect_queue(self, channel_name: str = None):
        try:
            await self.channel.declare_queue(channel_name, durable=True)
        except Exception as er:
            self.logger.exception(er)

    async def send_notification(self, event: BaseNote) -> BaseNote | None:
        event_data = event.dict()
        event_id = str(event_data['id'])
        if event.event.event_type != 'periodic':
            if await self.redis_client.setnx(event_id, 1) == 0:
                # Event ID already processed
                return None

        # Формирую специальный тип Exchange, позволяющий посылать через него на
        # несколько очередей сразу
        broadcasting_exchange = await self.channel.declare_exchange(
            'broadcast_exchange',
            ExchangeType.FANOUT,
            durable=True
        )

        self.broadcast = {
            await self.channel.declare_queue(
                f'{settings.queue}{queue_type}',
                durable=True
            ) for queue_type in event.event.broadcast_type
        }

        # Формирую привязку трех очередей к одному Exchange для броадкаста
        [await queue.bind(exchange='broadcast_exchange') for queue in self.broadcast]

        try:
            message = Message(body=event.json().encode(), delivery_mode=2)
            await broadcasting_exchange.publish(
                message,
                routing_key='',
                mandatory=True,
            )
            self.logger.info(f"Notification sent for event: {event_data['event']['event_type']}")
            return event

        except Exception as e:
            # Handle exception and requeue event for processing
            self.logger.exception(f"Error sending notification: {str(e)}")
            await self.redis_client.delete(event_id)

        finally:
            # Если не отвязать очереди, то в следующий раз сообщения будут направлены в те очереди, к
            # которым привязка уже есть, не зависимо от указанного event.event.broadcast_type
            [await queue_name.unbind(exchange='broadcast_exchange') for queue_name in self.broadcast]

    async def send_validated_notification(self, event: BaseNote):

        template = event.event.data
        validate_template(template)

        return await self.send_notification(event)


@lru_cache()
def get_notification_service(
        redis: Redis = Depends(get_redis),
        rabbit: tuple[Connection, AbstractChannel] = Depends(get_rabbit)
) -> NotificationService:
    return NotificationService(rabbit[0], rabbit[1], redis)
