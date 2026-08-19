from decimal import Decimal

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import RoleEnum, User


class WherePasswordException(Exception):
    pass



def _hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def _verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    async def add(self, data: dict) -> User:
        data = dict(data)  
        password = data.pop("password", None)

        user = User(**data)
        if password is not None:
            user.hashed_password = _hash_password(password)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        user = await self.session.get(User, user_id)
        if user is None:
            return False
        await self.session.delete(user)
        await self.session.commit()
        return True

    async def check_validated_password(self, parent_id: int, password: str) -> bool:
        user = await self.session.get(User, parent_id)
        if user is None or user.hashed_password is None:
            raise WherePasswordException(f"No password set for user {parent_id}")
        return _verify_password(password, user.hashed_password)

    async def search_child(self, element_id: int) -> User | None:
        """Возвращает User или None (не dict) — чище для isinstance-проверок в эндпоинтах."""
        stmt = select(User).where(User.id == element_id, User.role == RoleEnum.CHILD)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_capital(self, child_id: int, amount: Decimal) -> User | None:
        child = await self.search_child(child_id)
        if child is None:
            return None
        child.capital += amount
        await self.session.commit()
        await self.session.refresh(child)
        return child