from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    """schemas for token"""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: int = None


class Msg(BaseModel):
    """schemas for message"""
    msg: str


class VerificationCreate(BaseModel):
    """schemas for check email in registration"""
    user_id: int


class VerificationOut(BaseModel):
    """schemas for check email in registration"""
    link: UUID
