from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.authSchema import LoginRequest
from app.services.authService import login_user
from app.utils.dbUtil import get_db
from app.config import API_VERSION

router = APIRouter(prefix=f"{API_VERSION['v1']}", tags=["Authentication"])

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(request.identifier, request.password, db)