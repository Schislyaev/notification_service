import aioredis
# import sentry_sdk
import uvicorn as uvicorn
from aio_pika import connect_robust
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import events, notification
from core.logger import Logger
from core.settings import settings
from db import mongo, rabbit, redis
# from model.notifications import Event
from model.stored_note import Note
from scheduler import scheduler

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

    scheduler.scheduler = AsyncIOScheduler(

    )
    scheduler.scheduler.start()

    await init_beanie(
        database=mongo.client['notifications'],     # Имя коллекции
        document_models=[Note]
    )


@app.on_event('shutdown')
async def shutdown():
    if redis.redis:
        await redis.redis.close()

    if rabbit.connection:
        await rabbit.channel.close()
        await rabbit.connection.close()

    if mongo.client:
        mongo.client.close()

    if scheduler.scheduler:
        scheduler.scheduler.shutdown()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
