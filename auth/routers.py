from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from user.models import User, UserCreate, UserTokens, UserLogin
from user.crud import retrieve_user_by_email, add_user
from .utils import create_access_token, create_refresh_token, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/signup', response_model=User)
async def signup(user: UserCreate):
    check_user = await retrieve_user_by_email(user.email)
    if check_user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")

    new_user = await add_user(user.model_dump())
    return new_user

@router.post('/login', response_model=UserTokens)
async def login(data: UserLogin):
    user = await retrieve_user_by_email(data.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    hashed_pass = user['password']
    if not await verify_password(data.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    return {
        "access_token": await create_access_token(user['_id']),
        "refresh_token": await create_refresh_token(user['_id']),
    }
