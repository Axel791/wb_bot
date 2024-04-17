from app.db.base import Base

from app.models.mixins import UUIDMixin, TimestampedMixin
from sqlalchemy import Column, BigInteger, String


class TelegramUser(UUIDMixin, TimestampedMixin, Base):
    """Модель телеграм пользователя"""

    user_id = Column(
        BigInteger, nullable=False, unique=True, index=True, doc="ID пользователя"
    )
    username = Column(String, nullable=True, doc="Username")
    first_name = Column(String, nullable=True, doc="Имя пользователя")
    last_name = Column(String, nullable=True, doc="Фамилия пользователя")

    __tablename__ = "telegram_users"

    def __repr__(self) -> str:
        return f"Пользователь: {self.user_id}"
