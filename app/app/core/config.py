from enum import Enum

from pydantic import PostgresDsn, Field, computed_field
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Settings(BaseSettings):
    """Настройки проекта"""

    # region Настройки бота
    bot_token: str = Field(title="Токен бота")
    message_per_second: float = Field(title="Кол-во сообщений в секунду", default=1)
    log_level: LogLevel = Field(title="Уровень логирования", default=LogLevel.INFO)
    # endregion

    wb_api_key: str = Field(title="API ключ")
    base_url: str = Field(title="wb url")
    debug: bool = Field(title="Режим отладки", default=True)

    # region Настройки БД
    postgres_user: str = Field(title="Пользователь БД")
    postgres_password: str = Field(title="Пароль БД")
    postgres_host: str = Field(title="Хост БД")
    postgres_port: int = Field(title="Порт ДБ", default="5432")
    postgres_db: str = Field(title="Название БД")
    # endregion

    database_url: PostgresDsn | None = Field(title="Ссылка БД", default=None)

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        if self.database_url:
            return self.database_url
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=f"{self.postgres_db}",
        )

    class Config:
        env_file = ".env"


settings = Settings()
