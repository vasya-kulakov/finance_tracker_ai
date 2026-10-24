import os
from sqlalchemy import select
import bcrypt
from src.db.database import async_session_maker
from src.db.models import User, RoleEnum


async def init_db() -> None:
    '''Создаёт администратора по умолчанию, если его нет.'''
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.role == RoleEnum.ADMIN).limit(1)
        )
        if result.scalar_one_or_none() is not None:
            return

        admin = User(
            name='ADMIN',
            role=RoleEnum.ADMIN,
            hashed_password=bcrypt.hashpw("admin".encode(), bcrypt.gensalt()).decode('utf-8'),
            capital=0,
            parent_id=None,
        )
        session.add(admin)
        await session.commit()