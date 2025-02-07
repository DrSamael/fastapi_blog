from fastapi import APIRouter, HTTPException, Depends
from typing import List

from .schemas import Post, PostUpdate, PostCreate
from .crud import (add_post, update_post, retrieve_post, retrieve_posts, delete_post, retrieve_published_posts,
                   retrieve_current_user_posts)
from src.auth.deps import get_current_user, author_required, check_post_ownership
from src.user.schemas import User

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


@router.get("/user-posts", response_model=List[Post], dependencies=[Depends(get_current_user)])
async def current_user_posts(current_user: User = Depends(get_current_user)):
    return await retrieve_current_user_posts(current_user['_id'])


@router.get("/{post_id}", response_model=Post)
async def show_post(post_id: str):
    post = await retrieve_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.patch("/{post_id}", response_model=Post, dependencies=[Depends(get_current_user), Depends(author_required),
                                                               Depends(check_post_ownership)])
async def edit_post(post_id: str, post: PostUpdate):
    updated_post = await update_post(post_id, post.model_dump(exclude_unset=True))
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found or no changes made")
    return updated_post


@router.delete("/{post_id}", dependencies=[Depends(get_current_user), Depends(author_required),
                                           Depends(check_post_ownership)])
async def destroy_post(post_id: str):
    post = await delete_post(post_id)
    if post.deleted_count == 1:
        return {"detail": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")


# @router.get("/search/")
# async def search_posts(query: str):
#     search_body = {
#         "query": {
#             "multi_match": {
#                 "query": query,
#                 "fields": ["title", "content"],
#                 "fuzziness": "AUTO"
#             }
#         }
#     }
#
#     response = await es.search(index="blog_posts", body=search_body)
#     results = [{"id": hit["_id"], "title": hit["_source"]["title"], "content": hit["_source"]["content"]}
#                for hit in response["hits"]["hits"]]
#
#     return {"results": results}
