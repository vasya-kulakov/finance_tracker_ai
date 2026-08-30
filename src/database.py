from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.models import Base
from src.config import settings
DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, echo=False)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    """FastAPI dependency: session = Depends(get_session)"""
    async with async_session_maker() as session:
        yield session

async def create_all_tables() -> None:
    """
    Создаёт все таблицы (и связанные ENUM-типы) по текущим моделям.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
 
 
async def drop_all_tables() -> None:
    """
    Удаляет все таблицы. drop_all также сам убирает ENUM-типы
    (role_enum и т.п.), связанные с этими таблицами — в отличие
    от сырого DROP TABLE, который оставлял тип висеть в базе.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
 
 
async def reset_database() -> None:
    """Полный сброс схемы: drop + create заново, по текущим моделям."""
    await drop_all_tables()
    await create_all_tables()