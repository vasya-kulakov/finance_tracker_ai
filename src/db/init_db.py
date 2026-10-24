from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import User, RoleEnum


async def init_db(session: AsyncSession = await get_session()):
    '''Инициализация бд и создание администратора по умолчанию, если его нет.'''
    q1 = session.execute("SELECT * FROM users WHERE role = ADMIN")
    if q1 is None:
        admin = User(
            name="Admin",
            role=RoleEnum.ADMIN,
            hashed_password="admin",  # Здесь можно использовать хеширование пароля
            capital=0.00,
            parent_id=None
        )
        session.add(admin)
        await session.commit()
    
