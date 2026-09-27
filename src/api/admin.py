from fastapi import APIRouter, HTTPException

from src.db.database import create_all_tables, drop_all_tables, reset_database

router = APIRouter()


@router.post("/admin/create_tables")
async def create_tables():
    """Создаёт все таблицы по текущим моделям (если их ещё нет)."""
    try:
        await create_all_tables()
        return {"status": "success", "detail": "Таблицы созданы"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании таблиц: {str(e)}")


@router.post('/admin/reset')
async def r_database():
    """Сбрасывает бд до заводских."""
    try:
        await reset_database()
        return {'status': 'success', 'msg': 'Table was dropped and created'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error {str(e)}')


@router.post("/admin/drop_tables")
async def drop_tables():
    """Удаляет все таблицы (и связанные ENUM-типы)."""
    try:
        await drop_all_tables()
        return {"status": "success", "detail": "Таблицы удалены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении таблиц: {str(e)}")
