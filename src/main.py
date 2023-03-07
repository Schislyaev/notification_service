import aioredis
# import sentry_sdk
import uvicorn as uvicorn
from aio_pika import connect_robust
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import events, notification
from core.logger import LOGGING, Logger
from core.settings import settings
from db import mongo, rabbit, redis
# from model.notifications import Event
from model.stored_note import Note

logger = Logger(__name__)

# sentry_sdk.init(dsn=settings.settings.sentry_dsn, traces_sample_rate=1.0)

app = FastAPI(
    title=settings.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    openapi_tags=[
        {
            'name': 'Notification',
            'description': 'Реализация постановки сообщений в очередь'
        },
    ]
)

app.include_router(notification.router, prefix='/api/v1', tags=['Notification'])
app.include_router(events.router, prefix='/api/v1', tags=['Events'])


@app.on_event('startup')
async def startup():
    redis.redis = await aioredis.from_url(f'redis://{settings.redis_host}:{settings.redis_port}')

    rabbit.connection = await connect_robust(settings.rabbit_url)
    rabbit.channel = await rabbit.connection.channel()

    mongo.client = AsyncIOMotorClient(
        "mongodb://{host}:{port}".format(
            host=settings.mongo_host,
            port=settings.mongo_port,
        ),
        uuidRepresentation='standard',
    )
    await init_beanie(
        database=mongo.client['notifications'],     # Имя коллекции
        document_models=[Note]
    )

    # Тут пример поста в БД с методом beanie - для теста
    #
    # await Note(
    #     request_id='qwwwwwwwwwwwwWWWWWWWWWWWWWWWwwwwwwwwwwwww',
    #     event=Event(event_type="ugc", event_tz="string", data="string"),
    #     user_id='5421770f-dd22-467c-8a01-861237fdd159',
    #     email="user@example.com"
    # ).insert()

    print('ok')


@app.on_event('shutdown')
async def shutdown():
    if redis.redis:
        await redis.redis.close()

    if rabbit.connection:
        await rabbit.channel.close()
        await rabbit.connection.close()

    if mongo.client:
        mongo.client.close()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING
    )
