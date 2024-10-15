from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from .schemas import UserCreate, UserUpdate, UserOut
from .crud import add_user, retrieve_users, retrieve_user, update_user, delete_user
from auth.deps import admin_required

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserOut, dependencies=[Depends(admin_required)])
async def create_user(user: UserCreate):
    new_user = await add_user(user.model_dump())
    return new_user


@router.get("/", response_model=List[UserOut], dependencies=[Depends(admin_required)])
async def list_users():
    return await retrieve_users()


@router.get("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_required)])
async def show_user(user_id: str):
    user = await retrieve_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserOut, dependencies=[Depends(admin_required)])
async def edit_user(user_id: str, user: UserUpdate):
    updated_user = await update_user(user_id, user.model_dump(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or no changes made")
    return updated_user


@router.delete("/{user_id}", dependencies=[Depends(admin_required)])
async def destroy_user(user_id: str):
    user = await delete_user(user_id)
    if user.deleted_count == 1:
        return {"detail": "User deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
