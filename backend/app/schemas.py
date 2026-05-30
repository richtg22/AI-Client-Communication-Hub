from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SummaryCreate(BaseModel):
    raw_update: str

class SummaryResponse(BaseModel):
    id: int
    raw_update: str
    summary: str
    risks: str
    next_steps: str
    email_draft: str
    created_at: datetime

    class Config:
        from_attributes = True