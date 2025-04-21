from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from ..schemas.userSchema import CreateUserRequest, UserResponse
from ..utils.dbUtil import get_db
from typing import List
from ..services.userService import create_new_user, get_all_users

router = APIRouter(prefix="/users", tags=["Users"])
db_dependency = Depends(get_db)

# Fetch all users
@router.get("/", response_model=List[UserResponse])
def fetch_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)

# Registration
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def register_user(user_data: CreateUserRequest, db: Session = db_dependency):
    return create_new_user(user_data, db)

