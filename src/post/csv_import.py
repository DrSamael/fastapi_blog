from fastapi import HTTPException, UploadFile, status
import pandas as pd
from io import BytesIO

from src.post.crud import add_post
from src.user.schemas import User

REQUIRED_COLUMNS = {"title", "content"}


async def import_posts(file: UploadFile, current_user: User) -> int:
    contents = await file.read()
    try:
        df = pd.read_csv(BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Error reading CSV file: {e}")

    if not REQUIRED_COLUMNS.issubset(df.columns):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"CSV must contain columns: {', '.join(REQUIRED_COLUMNS)}")

    posts_data = df.to_dict(orient="records")

    created_posts = []
    for row in posts_data:
        post_data = {
            "title": row["title"],
            "content": row["content"],
            "published": False,
            "views": 0,
            "user_id": current_user["_id"]
        }
        post = await add_post(post_data, current_user["_id"])
        created_posts.append(post)

    return len(created_posts)
