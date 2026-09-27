from abc import ABC
from decimal import Decimal

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import RoleEnum, Transaction, Update_grade, User


class Repository(ABC):
    def add(self, data):
        pass

    def delete(self, id):
        pass

    def get_all(self):
        pass


class WherePasswordException(Exception):
    pass


def _hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def _verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


class UserRepository(Repository):
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


class TransactionRepository(Repository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict) -> Transaction:
        trans = Transaction(**data)
        self.session.add(trans)
        await self.session.commit()
        await self.session.refresh(trans)
        return trans

    async def delete(self, trans_id: int) -> bool:
        trans = await self.session.get(Transaction, trans_id)
        if trans is None:
            return False
        await self.session.delete(trans)
        await self.session.commit()
        return True

    async def get_all(self) -> list[Transaction]:
        result = await self.session.execute(select(Transaction))
        return list(result.scalars().all())


class GradeRepository(Repository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: dict) -> Update_grade:
        grade = Update_grade(**data)
        self.session.add(grade)
        await self.session.commit()
        await self.session.refresh(grade)
        return grade

    async def delete(self, grade_id: int) -> bool:
        grade = await self.session.get(Update_grade, grade_id)
        if grade is None:
            return False
        await self.session.delete(grade)
        await self.session.commit()
        return True

    async def get_all(self) -> list[Update_grade]:
        result = await self.session.execute(select(Update_grade))
        return list(result.scalars().all())

