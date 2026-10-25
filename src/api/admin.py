from fastapi import APIRouter, Depends, HTTPException
from src.db.models import RoleEnum
from src.services.db_admin_service import (
    create_tables_keep_admin,
    drop_tables_keep_admin,
    reset_database_keep_admin,
)
from .depends import get_current_active_user

def require_admin(user=Depends(get_current_active_user)):
    if user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")
    return user

router = APIRouter(dependencies=[Depends(require_admin)])


@router.post("/admin/create_tables")
async def create_tables():
    try:
        await create_tables_keep_admin()
        return {"status": "success", "detail": "Таблицы созданы"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании таблиц: {e}")