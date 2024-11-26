from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DocumentCreate(BaseModel):
    user_id: int
    title: str
    description: str


class DocumentUpdate(BaseModel):
    id: int
    user_id: int
    org_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    token_identifier: Optional[str] = None
    embedding: Optional[str] = None
    file_id: Optional[str] = None


class DocumentResponse(BaseModel):
    id: int
    user_id: int
    org_id: str
    title: str
    description: str
    token_identifier: str
    embedding: str
    file_id: str
