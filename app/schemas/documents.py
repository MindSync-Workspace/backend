from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MetaResponse(BaseModel):
    status: int
    message: str


class DocumentCreate(BaseModel):
    user_id: int
    title: str
    summary: Optional[str] = None
    org_id: Optional[str] = None
    embedding: Optional[str] = None


class DocumentUpdate(BaseModel):
    id: int
    user_id: int
    org_id: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    token_identifier: Optional[str] = None
    embedding: Optional[str] = None
    file_id: Optional[str] = None


class DocumentData(BaseModel):
    id: int
    user_id: int
    org_id: str
    title: str
    summary: str
    token_identifier: str
    embedding: str
    file_id: str


class DocumentResponse(BaseModel):
    meta: MetaResponse
    data: DocumentData


class DocumentsResponse(BaseModel):
    meta: MetaResponse
    data: List[DocumentData]
