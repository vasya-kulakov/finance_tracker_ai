import enum
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class RoleEnum(str, enum.Enum):
    PARENT = "PARENT"
    CHILD = "CHILD"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(SAEnum(RoleEnum, name="role_enum"), nullable=False)

    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)

    capital: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=Decimal("0.00"), server_default="0.00"
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "role": self.role.value,
            "capital": float(self.capital) if self.capital is not None else None,
            "parent_id": self.parent_id,
        }

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r} role={self.role}>"