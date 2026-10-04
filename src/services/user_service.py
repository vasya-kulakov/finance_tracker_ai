from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.repository import UserRepository
from src.security import verify_password, create_access_token, decode_access_token


async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
    """Ищет пользователя по имени (поле name в модели) в базе данных"""
    stmt = select(User).where(User.name == username)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
    """Аутентифицирует пользователя: проверяет, что такой есть и пароль верный"""
    user = await get_user_by_username(session, username)
    if not user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def create_user(session: AsyncSession, data: dict) -> User:
    """Создаёт пользователя через репозиторий (хеширование пароля внутри)"""
    repo = UserRepository(session)
    user = await repo.add(data)
    return user


def create_token_for_user(user: User) -> str:
    """Создаёт JWT токен для пользователя (sub = id)"""
    payload = {"sub": str(user.id), "name": user.name, "role": user.role.value}
    return create_access_token(payload)


def verify_token(token: str) -> Optional[dict]:
    """Декодирует и проверяет токен, возвращает payload или None"""
    return decode_access_token(token)
