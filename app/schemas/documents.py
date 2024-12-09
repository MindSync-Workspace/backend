from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MetaResponse(BaseModel):
    status: int
    message: str


class DocumentCreate(BaseModel):
    user_id: Optional[int] = None
    number: Optional[str] = None
    title: str
    summary: Optional[str] = None
    org_id: Optional[str] = None


class DocumentData(BaseModel):
    id: int
    user_id: int
    title: str
    summary: Optional[str]
    file_path: str
    file_size: int
    created_at: datetime
    updated_at: datetime


class DocumentUpdate(BaseModel):
    id: int
    user_id: int
    org_id: Optional[str] = None
    title: Optional[str] = None


class DocumentResponse(BaseModel):
    meta: MetaResponse
    data: DocumentData


class DocumentsResponse(BaseModel):
    meta: MetaResponse
    data: List[DocumentData]
