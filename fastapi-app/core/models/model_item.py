from core.models.model_base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Item(Base):
    item: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    remaked_description: Mapped[str] = mapped_column()
