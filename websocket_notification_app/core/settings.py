from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    project_name: str = 'Websocket notification app'

    grpc_host: str = 'localhost'
    grpc_port: int = 5051

    class Config:
        env_file_encoding = 'utf-8'
        case_sensitive = False


settings = Settings()
