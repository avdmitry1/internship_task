from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    max_overflow: int = 10
    poolsize: int = 5


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DataBaseConfig


settings = Settings()
