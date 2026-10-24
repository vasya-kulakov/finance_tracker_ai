from sqlalchemy import insert, inspect, select, text

from src.db.database import engine
from src.db.init_db import init_db
from src.db.models import Base, RoleEnum, User

users = User.__table__


async def _snapshot_admins(conn) -> list[dict]:
    """Читает администраторов до сброса. Если таблицы ещё нет, возвращает []."""
    exists = await conn.run_sync(lambda c: inspect(c).has_table(users.name))
    if not exists:
        return []
    result = await conn.execute(select(users).where(users.c.role == RoleEnum.ADMIN))
    return [dict(row) for row in result.mappings().all()]


async def _restore_admins(conn, admins: list[dict]) -> None:
    if not admins:
        return
    await conn.execute(insert(users), admins)
    await conn.execute(text(
        f"SELECT setval(pg_get_serial_sequence('{users.name}', 'id'), "
        f"(SELECT MAX(id) FROM {users.name}))"
    ))


async def _rebuild_keep_admin() -> None:
    async with engine.begin() as conn:  
        admins = await _snapshot_admins(conn)
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await _restore_admins(conn, admins)
    await init_db()  


async def create_tables_keep_admin() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 
    await init_db()


async def reset_database_keep_admin() -> None:
    await _rebuild_keep_admin()


async def drop_tables_keep_admin() -> None:
    await _rebuild_keep_admin()