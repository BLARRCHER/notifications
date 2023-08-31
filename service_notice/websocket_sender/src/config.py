from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    jwt_secret_key: str = Field("secret_jwt_key", env="WEBSOCKET_SENDER_JWT_KEY")
    debug: bool = Field(True, env="WEBSOCKET_SENDER_DEBUG")
    websocket_host: str = Field("localhost", env="WEBSOCKET_SENDER_HOST")
    websocket_port: str = Field(8888, env="WEBSOCKET_SENDER_PORT")
    rabbitmq_user: str = Field("user", env="RABBITMQ_NOTICE_USER")
    rabbitmq_password: str = Field("password", env="RABBITMQ_NOTICE_PASSWORD")
    rabbitmq_host: str = Field("localhost", env="RABBITMQ_NOTICE_HOST")
    rabbitmq_port: int = Field(5672, env="RABBITMQ_NOTICE_PORT")
    websocket_queue: str = "websocket"


settings = Settings()
