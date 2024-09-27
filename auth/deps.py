from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
import jwt
import dotenv
from pydantic import ValidationError

from user.crud import retrieve_user
from user.models import User


dotenv.load_dotenv()
reusable_oauth = OAuth2PasswordBearer(tokenUrl="/login", )

ALGORITHM = os.getenv('ALGORITHM')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')


async def get_current_user(token: str = Depends(reusable_oauth)):
    try:
        token_data = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)

        if datetime.fromtimestamp(token_data['exp']) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.exceptions.InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user: Union[dict[str, Any], None] = await retrieve_user(token_data['sub'])

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find user")

    return user

async def admin_required(current_user: User = Depends(get_current_user)):
    if current_user['role'] != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Admin has access to this resource")
    return current_user
