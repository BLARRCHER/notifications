from pathlib import Path

from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).parent.parent
ENV_FILE = BASE_DIR.parent / ".env.local"


class Settings(BaseSettings):
    project_name: str = "notice service:etl"

    pg_uri: str = Field(..., env="NOTICE_ETL_PG_URI")
    auth_service_uri: str = Field(..., env="NOTICE_ETL_AUTH_SERVICE_URI")
    auth_api_path: str = "/auth/v1/userinfo"
    redis_uri: str = Field(..., env="NOTICE_ETL_REDIS_URI")
    rabbitmq_uri: str = Field(..., env="NOTICE_ETL_RABBITMQ_URI")
    debug: bool = Field(True, env="NOTICE_ETL_DEBUG")
    secret_key: str = Field("secret_key", env="NOTICE_ETL_SECRET_KEY")

    jaeger_host_name: str = Field("localhost", env="JAEGER_HOST_NAME")
    jaeger_port: int = Field(6831, env="JAEGER_PORT")
    enable_tracer: bool = Field(False, env="ENABLE_TRACER")

    enable_sentry: bool = Field(False, env="ENABLE_SENTRY")
    sentry_dsn: str = Field("<sentry dsn>", env="SENTRY_DSN")
    release_version: str = Field("notice-service@1.0.0", env="RELEASE_VERSION")


settings = Settings(_env_file=ENV_FILE)
