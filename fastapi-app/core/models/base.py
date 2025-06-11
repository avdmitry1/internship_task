from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
import inflect

inflect_engine = inflect.engine()


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return inflect_engine.plural(cls.__name__.lower())

    id: Mapped[int] = mapped_column(primary_key=True)
