from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.token import Token, LoginForm
from src.services.user_service import authenticate_user
from src.security import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_session


router = APIRouter()

@router.post('/login', response_model=Token)
async def login(session: AsyncSession = Depends(get_session), form_data:LoginForm = Depends()) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(data={'sub': str(user.id)})
    return Token(access_token=access_token, token_type='bearer')