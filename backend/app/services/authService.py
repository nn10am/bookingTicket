from sqlalchemy.orm import Session
from ..models.userModel import User
from ..utils.authUtil import authenticate_user, generate_access_token
from ..utils.errorHandleUtil import login_error

# Service function to login an user an return an access token
def login_user(identifier: str, password: str, db: Session):
    user = authenticate_user(identifier, password, db)

    if not user:
        login_error()
    
    access_token = generate_access_token(user.username, user.id, user.is_admin)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    

        