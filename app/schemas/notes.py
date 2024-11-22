from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class NoteCreate(BaseModel):
    userId: int
    text: str


class NoteUpdate(BaseModel):
    text: Optional[str] = None


class NoteResponse(BaseModel):
    id: int
    text = str
    userId = str
    embedding: Optional[List[float]] = None
    tokenIdentifier: Optional[str] = None
    created_at: datetime
    modified_at: datetime
