from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Union, Any
from fastapi import Request

from user.schemas import User, UserCreate, UserTokens, UserOut
from user.crud import retrieve_user_by_email, add_user, retrieve_user
from .utils import verify_password, decode_refresh_token, create_token, validate_token
from .deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/signup', response_model=UserOut)
async def signup(user: UserCreate):
    check_user = await retrieve_user_by_email(user.email)
    if check_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")

    new_user = await add_user(user.model_dump())
    return new_user


@router.post('/login', response_model=UserTokens)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await retrieve_user_by_email(data.username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    hashed_pass = user['password']
    if not await verify_password(data.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    return {
        "access_token": await create_token(user['_id'], None, 'access_token'),
        "refresh_token": await create_token(user['_id'], None, 'refresh_token'),
    }


@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user


@router.get("/refresh-token", response_model=UserTokens)
async def refresh_access_token(request: Request):
    refresh_token = request.headers.get('refresh-token')
    if refresh_token is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Refresh token missing")

    token_data = await validate_token(refresh_token, 'refresh_token')
    user: Union[dict[str, Any], None] = await retrieve_user(token_data['sub'])

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")

    return {
        "access_token": await create_token(user['_id'], None, 'access_token'),
        "refresh_token": await create_token(user['_id'], None, 'refresh_token')
    }
