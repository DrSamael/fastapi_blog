from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from .models import User, UserCreate, UserUpdate, UserOut
from .crud import add_user, retrieve_users, retrieve_user, update_user, delete_user
from auth.deps import get_current_user, admin_required


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=User, dependencies=[Depends(admin_required)])
async def create_user(user: UserCreate):
    new_user = await add_user(user.model_dump())
    return new_user

@router.get("/", response_model=List[UserOut], dependencies=[Depends(admin_required)])
async def list_users():
    return await retrieve_users()

@router.get("/{id}", response_model=User, dependencies=[Depends(admin_required)])
async def show_user(id: str):
    user = await retrieve_user(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.patch("/{id}", response_model=UserOut, dependencies=[Depends(admin_required)])
async def edit_user(id: str, user: UserUpdate):
    updated_user = await update_user(id, user.model_dump(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or no changes made")
    return updated_user

@router.delete("/{id}", dependencies=[Depends(admin_required)])
async def destroy_user(id: str):
    user = await delete_user(id)
    if user.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
