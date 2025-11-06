from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, status
from typing import List

from .csv_import import import_posts
from .schemas import Post, PostUpdate, PostCreate, SearchPost, PostStatsResponse
from .crud import (add_post, update_post, retrieve_post, retrieve_posts, delete_post, retrieve_published_posts,
                   retrieve_current_user_posts, get_post_stats)
from src.auth.deps import get_current_user, author_required, check_post_ownership, admin_required
from src.user.schemas import User
from src.search.crud import search_post_in_elasticsearch

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=Post, dependencies=[Depends(get_current_user), Depends(author_required)])
async def create_post(post: PostCreate, current_user: User = Depends(get_current_user)):
    new_post = await add_post(post.model_dump(), current_user['_id'])
    return new_post


@router.get("/", response_model=List[Post])
async def list_posts():
    return await retrieve_posts({})


@router.get("/published", response_model=List[Post])
async def published_list_posts():
    return await retrieve_published_posts()


@router.get("/stats", response_model=PostStatsResponse, dependencies=[Depends(admin_required)])
async def posts_stats():
    return await get_post_stats()


@router.get("/user-posts", response_model=List[Post], dependencies=[Depends(get_current_user)])
async def current_user_posts(current_user: User = Depends(get_current_user)):
    return await retrieve_current_user_posts(current_user['_id'])


@router.get("/{post_id}", response_model=Post)
async def show_post(post_id: str):
    post = await retrieve_post(post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@router.patch("/{post_id}", response_model=Post, dependencies=[Depends(get_current_user), Depends(author_required),
                                                               Depends(check_post_ownership)])
async def edit_post(post_id: str, post: PostUpdate):
    updated_post = await update_post(post_id, post.model_dump(exclude_unset=True))
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or no changes made")
    return updated_post


@router.delete("/{post_id}", dependencies=[Depends(get_current_user), Depends(author_required),
                                           Depends(check_post_ownership)])
async def destroy_post(post_id: str):
    post = await delete_post(post_id)
    if post.deleted_count == 1:
        return {"detail": "Post deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.post("/search", response_model={})
async def search_posts(query: SearchPost):
    search_body = {
        "query": {
            "multi_match": {
                "query": query.query,
                "fields": ["title", "content"],
                "fuzziness": "AUTO"
            }
        }
    }
    result = await search_post_in_elasticsearch(search_body)
    return {"result": result}


@router.post("/upload", response_model={},
             dependencies=[Depends(get_current_user), Depends(author_required)])
async def upload_posts(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only CSV files are allowed")

    result = await import_posts(file, current_user)

    return {"detail": f"Created posts count: {result}"}
