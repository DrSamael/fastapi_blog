from fastapi import APIRouter, HTTPException, Depends
from typing import List

from .schemas import Author, AuthorCreate, AuthorUpdate
from .crud import retrieve_authors, add_autor, retrieve_author, update_author, delete_author
from src.auth.deps import admin_required, get_current_user
from src.user.schemas import User
from src.author.services.validator import validate_author_data

router = APIRouter(prefix="/authors", tags=["authors"])


@router.post("/", response_model=Author, dependencies=[Depends(admin_required)])
async def create_author(author: AuthorCreate):
    await validate_author_data(author.user_id)
    new_author = await add_autor(author.model_dump())
    return new_author


@router.get("/", response_model=List[Author], dependencies=[Depends(admin_required)])
async def list_authors():
    return await retrieve_authors()


@router.get("/user-author", response_model=List[Author], dependencies=[Depends(get_current_user)])
async def current_user_author(current_user: User = Depends(get_current_user)):
    return await retrieve_authors(current_user['_id'])


@router.get("/{author_id}", response_model=Author, dependencies=[Depends(admin_required)])
async def show_author(author_id: str):
    author = await retrieve_author(author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.patch("/{author_id}", response_model=Author, dependencies=[Depends(admin_required)])
async def edit_author(author_id: str, author: AuthorUpdate):
    updated_author = await update_author(author_id, author.model_dump(exclude_unset=True))
    if updated_author is None:
        raise HTTPException(status_code=404, detail="Author not found or no changes made")
    return updated_author


@router.delete("/{author_id}", dependencies=[Depends(admin_required)])
async def destroy_author(author_id: str):
    author = await delete_author(author_id)
    if author.deleted_count == 1:
        return {"detail": "Author deleted successfully"}
    raise HTTPException(status_code=404, detail="Author not found")
