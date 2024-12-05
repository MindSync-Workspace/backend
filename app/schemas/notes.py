from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MetaResponse(BaseModel):
    status: int
    message: str


class NoteData(BaseModel):
    id: int
    text: str
    user_id: int
    org_id: Optional[int] = None
    created_at: datetime
    modified_at: datetime


class NoteCreate(BaseModel):
    user_id: Optional[int] = None
    org_id: Optional[int] = None
    number: Optional[str] = None
    text: str


class NoteSearch(BaseModel):
    # org_id: Optional[int] = None
    # number: Optional[str] = None
    n_items: int
    text: str


class NoteUpdate(BaseModel):
    user_id: int
    org_id: Optional[int] = None
    text: str


class NoteResponse(BaseModel):
    meta: MetaResponse
    data: NoteData


class NotesResponse(BaseModel):
    meta: MetaResponse
    data: List[NoteData]
