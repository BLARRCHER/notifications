from datetime import time

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    send_from_email: str = Field("test@example.com", env="EMAIL_SENDER_FROM_EMAIL")
    debug: bool = Field(True, env="EMAIL_SENDER_DEBUG")
    rabbitmq_user: str = Field("user", env="RABBITMQ_NOTICE_USER")
    rabbitmq_password: str = Field("password", env="RABBITMQ_NOTICE_PASSWORD")
    rabbitmq_host: str = Field("localhost", env="RABBITMQ_NOTICE_HOST")
    rabbitmq_port: int = Field(5672, env="RABBITMQ_NOTICE_PORT")
    email_queue: str = "email"
    email_dlq: str = "email-dlq"
    max_retries: int = 3
    retry_interval_ms: int = 5000
    sendgrid_api_key: str = "default_for_local_debug"
    send_after_time: time = time(hour=9, minute=0)
    send_before_time: time = time(hour=21, minute=0)


settings = Settings()
