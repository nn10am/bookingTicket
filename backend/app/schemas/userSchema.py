from pydantic import BaseModel, EmailStr

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool

    class Config:
        from_attributes = True