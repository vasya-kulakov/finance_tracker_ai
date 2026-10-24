from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.docs.docs import Docs
from src.models.roles import Children, Parent
from src.services.family_service import FamilyService
from .depends import get_current_active_user
router = APIRouter()


@router.get('/family')
async def show_family(session: AsyncSession = Depends(get_session)):
    service = FamilyService(session)
    family = await service.get_family()
    return {"family": family}


@router.put('/family/add_parent')
async def add_parent(
    parent: Annotated[Parent, Body(..., example=Docs.parent_docs_json_format)],
    session: AsyncSession = Depends(get_session),
):
    service = FamilyService(session)
    created = await service.add_parent(parent)
    return {
        "message": "Parent added successfully",
        "parent": created,
    }


@router.put('/family/add_child')
async def add_child(
    child: Annotated[Children, Body(..., example=Docs.child_docs_json_format)],
    session: AsyncSession = Depends(get_session),
):
    service = FamilyService(session)
    created = await service.add_child(child)
    return {
        "message": "Child added successfully",
        "child": created,
    }


@router.post('/family/{id_child}')
async def add_child_capital(
    id_child: Annotated[int, Path(..., title='Child id')],
    current_user: Parent = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
    money: Annotated[int, Path(..., title='Money', example=100)] = 100
):
    service = FamilyService(session)

    try:
        updated = await service.add_capital(id_child, current_user, Decimal(money))
    except ValueError as exc:
        if str(exc) == "Child id not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Child id not found",
            ) from exc
    return {
        'msg': 'Capital was added successfully',
        'child': updated,
    }