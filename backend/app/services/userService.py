from sqlalchemy.orm import Session
from passlib.context import CryptContext
from email_validator import validate_email, EmailNotValidError
from ..models.userModel import User
from ..schemas.userSchema import CreateUserRequest, UserResponse
from ..utils.errorHandleUtil import (
    user_exists_error,
    not_found_error,
    invalid_data_error,
    validate_username_length,
    validate_email_length,
    validate_password_length,
    generic_error
)
from ..utils.authUtil import bcrypt_context, get_user_by_field, hash_password

# Fetch all users
def get_all_users(db: Session):
    try:
        users = db.query(User).all()
        return users
    except Exception as e:
        print("Error fetching users:", str(e))
        generic_error()

# Get user by id
def get_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        not_found_error("User")
    
    return user

# Register new user
def create_new_user(create_user_request: CreateUserRequest, db: Session):
    try:
        # Validate field lengths:
        validate_username_length(create_user_request.username)
        validate_email_length(create_user_request.email)
        validate_password_length(create_user_request.password)

        # Validate email format:
        try:
            validate_email(create_user_request.email)
        except EmailNotValidError as e:
            invalid_data_error(str(e))

        # Check username
        username_lower = create_user_request.username.lower()
        if get_user_by_field('username', username_lower, db):
            raise user_exists_error("Username")

        # Check email
        if get_user_by_field('email', create_user_request.email, db):
            raise user_exists_error("Email")
        
        # Hash the password:
        hashed_password = hash_password(create_user_request.password)

        # Create user instance
        user = User(
            username=create_user_request.username.lower(),
            email=create_user_request.email,
            hashed_password = hashed_password,
            is_admin = False
        )

        # commit to DB
        db.add(user)
        db.commit()
        db.refresh(user)

        return {"message": "User created successfully!"}
    except Exception as e:
        print("Error during registration: ", str(e))
        generic_error()