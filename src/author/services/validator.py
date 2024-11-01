from fastapi import HTTPException, status

from src.author.crud import retrieve_author_by_user_id


async def check_author_existence(user_id: str):
    existing_author = await retrieve_author_by_user_id(user_id)
    if existing_author:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already has an author")
    return user_id
