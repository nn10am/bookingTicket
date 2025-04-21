from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    identifier: str
    password: str

