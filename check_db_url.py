from sentry_sdk import session
from sqlalchemy.orm import Mapped, mapped_column

from config import settings
from sqlalchemy import select

from database import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str]

row = session.execute(select(User)).first()

print(select(User))

print("Async database URL:", settings.async_database_url)