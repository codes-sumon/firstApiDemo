from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = {"from_attributes": True}

class UserLogin(BaseModel):
    username: str
    password: str