from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


DATABASE_URL = 'postgresql+asyncpg://admin:admin@127.0.0.1:5432/finance_db'

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_session() -> AsyncSession:
    """Dependency для FastAPI: Depends(get_session)"""
    async with async_session() as session:
        yield session