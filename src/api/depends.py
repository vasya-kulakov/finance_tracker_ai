from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.security import decode_access_token
from src.db.database import get_session
from src.db.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



async def get_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> Optional[User]:
    """FastAPI dependency: user = Depends(get_user)"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    user = await session.get(User, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user

async def get_current_active_user(
    current_user: User = Depends(get_user)
) -> User:
    return current_user