from decimal import Decimal
from typing import Annotated

from fastapi import Body, Depends, FastAPI, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session, create_all_tables, drop_all_tables, reset_database
from src.docs import Docs
from src.repository import UserRepository, WherePasswordException
from src.roles import Children, Parent

#####################
app = FastAPI()     #
#####################
# db = DataBase()

# Help Me please !!!

@app.get('/')
async def welcome_to_finance_tracker(session: AsyncSession = Depends(get_session)):
    return {
        'msg': 'welcome to my finance tracker. '
        'This project is only backend part of app. For use API I will recommended use a /docs path',
        'main_page': 1
    }

@app.get('/family')
async def show_family(session: AsyncSession = Depends(get_session)):
    
    repo = UserRepository(session)
    family = await repo.get_all()
    return {
        'family': [user.to_dict() for user in family]
    }

@app.post("/admin/create_tables")
async def create_tables():
    """Создаёт все таблицы по текущим моделям (если их ещё нет)."""
    try:
        await create_all_tables()
        return {"status": "success", "detail": "Таблицы созданы"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при создании таблиц: {str(e)}")
 
 
@app.post("/admin/drop_tables")
async def drop_tables():
    """Удаляет все таблицы (и связанные ENUM-типы)."""
    try:
        await drop_all_tables()
        return {"status": "success", "detail": "Таблицы удалены"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении таблиц: {str(e)}")


@app.get('/admin/maketest')
async def make_tests():
    '''Прогоняет тесты из папки tests'''
    

@app.put('/family/add_parent')
async def add_parent(
    parent: Annotated[Parent, Body(..., example=Docs.parent_docs_json_format)],
    session: AsyncSession = Depends(get_session),
):
    repo = UserRepository(session)
    data = parent.model_dump()
    data['role'] = 'PARENT'
    created = await repo.add(data)
    return {
        "message": "Parent added successfully",
        "parent": created.to_dict(),
    }


@app.put('/family/add_child')
async def add_child(
    child: Annotated[Children, Body(..., example=Docs.child_docs_json_format)],
    session: AsyncSession = Depends(get_session),
):
    repo = UserRepository(session)
    data = child.model_dump()
    data['role'] = 'CHILD'
    data['capital'] = 0
    created = await repo.add(data)
    return {
        "message": "Child added successfully",
        "child": created.to_dict(),
    }


@app.post('/family/{id_child}')
async def add_child_capital(
    id_child: Annotated[int, Path(..., title='Child id')],
    token: Annotated[str, Body(..., title='Password - need to password for id parent, who`s be in children info')],
    money: Annotated[int, Body(..., title='How much we get a child')],
    session: AsyncSession = Depends(get_session),
):
    repo = UserRepository(session)

    child = await repo.search_child(id_child)
    if child is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child id not found",
        )

    try:
        is_valid = await repo.check_validated_password(child.parent_id, token)
    except WherePasswordException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parent has no password set",
        )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Error parent password",
        )

    updated = await repo.add_capital(id_child, Decimal(money))
    return {
        'msg': 'Capital was added successfully',
        'child': updated.to_dict(),
    }