from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DocumentCreate(BaseModel):
    user_id: int
    title: str
    description: str


class NoteUpdate(BaseModel):
    user_id: int
    text: str


class NoteResponse(BaseModel):
    id: int
    text: str
    user_id: str
    embedding: Optional[List[float]] = None
    token_identifier: Optional[str] = None
    created_at: datetime
    modified_at: datetime
