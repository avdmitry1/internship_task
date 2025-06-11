from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import settings


class DataBaseHelper:
    """
    Помічник для роботи з асинхронною базою даних через SQLAlchemy.
    """

    def __init__(
        self,
        url: str,
        echo: bool = False,
        max_overflow: int = 10,
        pool_size: int = 5,
    ):
        # Створюємо асинхронний движок бази даних з налаштуваннями пулу з'єднань
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        # Створюємо фабрику сесій для роботи з базою даних
        self.session_factory = async_sessionmaker(
            bind=self.engine,  # Прив'язуємо до нашого движка
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self):
        """
        Закриває всі з'єднання з базою даних та звільняє ресурси.
        Цей метод слід викликати при завершенні роботи програми
        для коректного закриття всіх підключень до бази даних.
        """
        await self.engine.dispose()

    async def get_session(self):
        """
        Повертає сесію для роботи з базою даних.
        """
        async with self.session_factory() as session:
            yield session


dp_helper = DataBaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.poolsize,
)
