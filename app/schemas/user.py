from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from datetime import datetime
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    @model_validator(mode="after")
    def validate_password_bytes(self):
        if len(self.password.encode('utf-8')) > 72:
            raise ValueError("Password exceeds maximum length of 72 bytes")
        return self

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    # Updated to Pydantic V2 format
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str