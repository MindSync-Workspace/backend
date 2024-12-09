from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MetaResponse(BaseModel):
    status: int
    message: str


class WhatsappCreate(BaseModel):
    user_id: int
    org_id: Optional[int] = None


class WhatsappUpdate(BaseModel):
    user_id: Optional[int] = None
    org_id: Optional[int] = None
    number: Optional[str] = None
    secret_key: Optional[str] = None


class WhatsappData(BaseModel):
    id: int
    user_id: int
    number: Optional[str] = None
    org_id: Optional[int] = None
    secret_key: Optional[str] = None
    created_at: datetime
    modified_at: datetime


class WhatsappResponse(BaseModel):
    meta: MetaResponse
    data: WhatsappData
