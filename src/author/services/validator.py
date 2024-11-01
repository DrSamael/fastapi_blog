from fastapi import HTTPException, status

from src.author.crud import retrieve_author_by_user_id
from src.user.crud import retrieve_user


async def validate_author_data(user_id: str):
    await _check_author_existence(user_id)
    await _check_user_existence(user_id)


async def _check_author_existence(user_id: str):
    existing_author = await retrieve_author_by_user_id(user_id)
    if existing_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already has an author")
    return user_id


async def _check_user_existence(user_id: str):
    existing_user = await retrieve_user(user_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist")
    return user_id
