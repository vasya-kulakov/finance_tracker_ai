from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_session
from src.db.repository import TransactionRepository

router = APIRouter()


@router.get('/transactions')
async def get_transactions(session: AsyncSession = Depends(get_session)):
    try:
        repo = TransactionRepository(session)
        transactions = await repo.get_all()
        return {
            'transactions': [transaction.to_dict() for transaction in transactions]
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f'Error {str(exc)}') from exc
