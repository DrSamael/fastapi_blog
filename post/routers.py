from fastapi import APIRouter, HTTPException, Depends
from typing import List

from .models import Post, PostCreate, PostUpdate
from .crud import add_post, update_post, retrieve_post, retrieve_posts, delete_post
from auth.deps import get_current_user


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=Post, dependencies=[Depends(get_current_user)])
async def create_post(post: PostCreate):
    new_post = await add_post(post.model_dump())
    return new_post

@router.get("/", response_model=List[Post])
async def list_posts():
    return await retrieve_posts()

@router.get("/{id}", response_model=Post)
async def show_post(id: str):
    post = await retrieve_post(id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.patch("/{id}", response_model=Post, dependencies=[Depends(get_current_user)])
async def edit_post(id: str, post: PostUpdate):
    updated_post = await update_post(id, post.model_dump(exclude_unset=True))
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found or no changes made")
    return updated_post

@router.delete("/{id}", dependencies=[Depends(get_current_user)])
async def destroy_post(id: str):
    post = await delete_post(id)
    if post.deleted_count == 1:
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")
