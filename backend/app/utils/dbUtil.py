from ..db.session import SessionLocal
from sqlalchemy.orm import Session
from ..models.userModel import User

def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to get user by email or username
def get_user_by_field(field: str, value: str, db: Session):
    if field not in ['username', 'email']:
        raise ValueError("Field must be 'username' or 'email'.")
    
    return db.query(User).filter(getattr(User, field) == value).first()