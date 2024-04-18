from pydantic import BaseModel, Field


class TelegramUserEntity(BaseModel):
    """Модель пользователя"""

    user_id: int = Field(title="ID пользователя")
    username: str | None = Field(title="Username", default=None)
    first_name: str | None = Field(title="Имя", default=None)
    last_name: str | None = Field(title="Фамилия", default=None)
