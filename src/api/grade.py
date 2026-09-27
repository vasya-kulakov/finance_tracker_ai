from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.db.repository import GradeRepository

router = APIRouter()

@router.get('/grades')
async def get_grades(session: AsyncSession = Depends(get_session)):
    try:
        repo = GradeRepository(session)
        transactions = await repo.get_all()
        return {
            'transactions': [transaction.to_dict() for transaction in transactions]
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f'Error {str(exc)}') from exc