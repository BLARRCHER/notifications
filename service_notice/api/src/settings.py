from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field("Producer", env="UGC_PROJECT_NAME")
    producer_dsn: str = Field(env="RABBITMQ_NOTICE_URI")
    queue_name: str = Field("notice", env="QUEUE_NAME")
    enable_tracer: bool = Field(False, env="ENABLE_TRACER")
    jaeger_host_name: str = Field("localhost", env="JAEGER_HOST_NAME")
    jaeger_port: int = Field(6831, env="JAEGER_PORT")
    debug: bool = Field(True, env="UGC_DEBUG")


settings = Settings(_env_file="../.env")
