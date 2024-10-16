from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
import dotenv
from pydantic import ValidationError
from bson import ObjectId

from user.crud import retrieve_user
from user.schemas import User
from user.enums import UserRoles
from post.crud import retrieve_post
from .utils import decode_access_token

dotenv.load_dotenv()
reusable_oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")


def validate_object_id(post_id: str):
    try:
        return ObjectId(post_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{post_id} is not a valid ObjectId.")


async def get_current_user(token: str = Depends(reusable_oauth)):
    try:
        token_data = await decode_access_token(token)

        if datetime.fromtimestamp(token_data['exp']) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
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
    if current_user['role'] != UserRoles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Admin has access to this resource")
    return current_user


async def author_required(current_user: User = Depends(get_current_user)):
    if current_user['role'] not in [UserRoles.author, UserRoles.admin]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Author has access to this resource")
    return current_user


async def check_post_ownership(post_id: str, current_user: User = Depends(get_current_user)):
    post = await retrieve_post(post_id)

    if not post:
        return
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if current_user['role'] == UserRoles.admin:
        return post

    if post['user_id'] != current_user['_id']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to modify this post")
    return post
