from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta, datetime
from passlib.context import CryptContext
from jose import jwt, JWTError # type: ignore
from email_validator import validate_email, EmailNotValidError
from ..models.userModel import User
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from ..utils.dbUtil import get_user_by_field
from ..db.session import get_db
import os

# Constants
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
SALT = os.getenv("SALT")

# TOKEN EXPIRES
ACCESS_TOKEN_EXPIRE_MINUTES = 20

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Apply salt password
def apply_salt(password: str) -> str:
    if not SALT:
        raise ValueError("SALT not set in the environment variables.")
    return password + SALT

# Hashing password
def hash_password(password: str) -> str:
    salted_pass = apply_salt(password)
    return bcrypt_context.hash(salted_pass)

# Verify password
def verify_password(plain_pass: str, hashed_pass: str) -> bool:
    salted_pass = apply_salt(plain_pass)
    return bcrypt_context.verify(salted_pass, hashed_pass)

# Authenticate user
def authenticate_user(identifier: str, password: str, db: Session):
    try:
        # Treat identifer as 'email'
        validate_email(identifier)
        user = get_user_by_field('email', identifier, db)
    except EmailNotValidError:
        # If not 'email', treat as 'username'
        user = get_user_by_field('username', identifier, db)
    
    if not user or not verify_password(password, user.hashed_password):
        return False

    return user

# Generate Access Token
def generate_access_token(username: str, user_id: int, is_admin: bool):
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "id": user_id,
        "is_admin": is_admin,
        "exp": expire_time
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Get current user
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_field('id', user_id, db)
    if user is None:
        raise credentials_exception
    return user