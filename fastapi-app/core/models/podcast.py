from core.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Podcast(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    host: Mapped[str] = mapped_column()
