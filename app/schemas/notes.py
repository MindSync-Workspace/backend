from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NoteCreate(BaseModel):
    user_id: int
    org_id: Optional[int] = None
    text: str


class NoteUpdate(BaseModel):
    user_id: int
    org_id: Optional[int] = None
    text: str


class NoteResponse(BaseModel):
    id: int
    text: str
    user_id: str
    org_id: Optional[int] = None
    embedding: Optional[List[float]] = None
    token_identifier: Optional[str] = None
    created_at: datetime
    modified_at: datetime
