from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatCreate(BaseModel):
    document_id: int
    token_identifier: str
    is_human: bool
    text: str


class ChatUpdate(BaseModel):
    token_identifier: Optional[str] = None
    is_human: Optional[bool] = None
    text: Optional[str] = None


class ChatResponse(BaseModel):
    id: int
    document_id: int
    token_identifier: str
    is_human: bool
    text: str
    created_at: datetime
    modified_at: datetime
