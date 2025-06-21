from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings


class DataBaseHelper:
    # Constructor
    def __init__(
        self,
        url: str,
        echo: bool = False,
        max_overflow: int = 10,
        pool_size: int = 5,
    ):
        # Create the database engine
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        # Create the session factory
        self.session_factory = async_sessionmaker(
            bind=self.engine,  # Прив'язуємо до нашого движка
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    # Method to close the engine
    async def dispose(self):
        await self.engine.dispose()

    # Method to get a session
    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_helper = DataBaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size,
)
