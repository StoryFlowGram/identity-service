from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import func, CheckConstraint
from sqlalchemy.types import Integer, BigInteger, String, DateTime
from app.infrastructure.database.base import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True, doc="Телеграмовский id")
    google_id: Mapped[str] = mapped_column(String, unique=True, nullable=True, doc="sub из id-токена гугла")
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True, doc="гугловский email ")
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    registred_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())  
    
    
    @validates("telegram_id")
    def validate_telegram_id(self, key, telegram_id):
        if telegram_id is not None and telegram_id < 0:
            raise ValueError("Telegram id должен быть больше нуля")
        elif not telegram_id:
            raise ValueError("Telegram id не может быть пустым")
        return telegram_id
    

    @validates("email")
    def validates_email(self, key, email):
        if email is not None and "@" not in email:
            raise ValueError("Адрес почты не может быть без @")
        return email
    
    @validates("first_name")
    def validate_first_name(self, key, first_name):
        if not first_name:
            raise ValueError("Имя не может быть пустым")
        return first_name
    
    __table_args__ = (
        CheckConstraint("telegram_id IS NULL OR telegram_id > 0", name="telegram_id_positive"),
        CheckConstraint("first_name IS NOT NULL", name="first_name_not_null"),
    )

    def repr(self):
        return f"User(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, telegram_id={self.telegram_id}, google_id={self.google_id}, email={self.email}), registred_at={self.registred_at})"