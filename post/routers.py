from fastapi import APIRouter, HTTPException
from typing import List
from .models import Post, PostCreate
from .crud import add_post, update_post, retrieve_post, retrieve_posts

# Create the API router
router = APIRouter()


@router.post("/posts/", response_model=Post)
async def create_post(post: PostCreate):
    new_post = await add_post(post.model_dump())
    return new_post

@router.get("/posts/", response_model=List[Post])
async def list_posts():
    return await retrieve_posts()

@router.get("/posts/{id}", response_model=Post)
async def show_post(id: str):
    post = await retrieve_post(id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/posts/{id}", response_model=Post)
async def edit_post(id: str, post: PostCreate):
    updated_post = await update_post(id, post.model_dump())
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found or no changes made")
    return updated_post

@router.delete("/posts/{id}")
async def delete_post(id: str):
    post = await delete_post(id)
    if post.deleted_count == 1:
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")
