from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas.authSchema import LoginRequest
from ..services.authService import login_user
from ..utils.dbUtil import get_db

router = APIRouter()

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request.identifier, request.password, db)