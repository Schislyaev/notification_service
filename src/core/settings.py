import pathlib

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    log_level: str = 'DEBUG'
    project_name: str = 'Notification service'
    grpc_host: str = 'localhost'
    grpc_port: int = 5051

    redis_host: str = '127.0.0.1'
    redis_port: int = 6379

    rabbit_url: str = 'amqp://127.0.0.1/'
    channel_ugc: str = 'notification.send_like'
    channel_periodic: str = 'notification.send_weekend_news'
    channel_handmade: str = 'notification.send_personal_note'

    mongo_host: str = 'localhost'
    mongo_port: int = 27017

    jwt_secret: SecretStr = ''
    jwt_algorithm: SecretStr = ''

    project_root_path = str(pathlib.Path(__file__).parent.parent.parent)

    sentry_dsn: str = 'https://3ec181e0dd36402fa2d93e20390d9caf@o4504700580790272.ingest.sentry.io/4504700581642240'

    class Config:
        env_file = f'{str(pathlib.Path(__file__).parent.parent.parent)}/.env.example'
        env_file_encoding = 'utf-8'
        case_sensitive = False


settings = Settings()
