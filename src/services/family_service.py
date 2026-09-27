from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repository import UserRepository, WherePasswordException
from src.models.roles import Children, Parent


class FamilyService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def get_family(self):
        family = await self.repo.get_all()
        return [user.to_dict() for user in family]

    async def add_parent(self, parent: Parent):
        data = parent.model_dump()
        data["role"] = "PARENT"
        created = await self.repo.add(data)
        return created.to_dict()

    async def add_child(self, child: Children):
        data = child.model_dump()
        data["role"] = "CHILD"
        data["capital"] = 0
        created = await self.repo.add(data)
        return created.to_dict()

    async def add_capital(self, child_id: int, token: str, money: Decimal):
        child = await self.repo.search_child(child_id)
        if child is None:
            raise ValueError("Child id not found")

        try:
            is_valid = await self.repo.check_validated_password(child.parent_id, token)
        except WherePasswordException as exc:
            raise ValueError("Parent has no password set") from exc

        if not is_valid:
            raise PermissionError("Error parent password")

        updated = await self.repo.add_capital(child_id, money)
        return updated.to_dict()
