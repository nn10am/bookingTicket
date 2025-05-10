from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from ..schemas.userSchema import CreateUserRequest, UserResponse
from ..utils.dbUtil import get_db
from typing import List
from ..services.userService import create_new_user, get_all_users, get_user_by_id

router = APIRouter(prefix="/users", tags=["Users"])
db_dependency = Depends(get_db)

# Fetch all users
@router.get("/", response_model=List[UserResponse])
async def fetch_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)

# Get an user by id
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(db, user_id)

# Registration
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: CreateUserRequest, db: Session = db_dependency):
    return create_new_user(user_data, db)

