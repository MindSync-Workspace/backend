from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MetaResponse(BaseModel):
    status: int
    message: str


class ChatData(BaseModel):
    id: int
    document_id: int
    # token_identifier: str
    org_id: int
    is_human: bool
    text: str
    created_at: datetime
    modified_at: datetime


class ChatCreate(BaseModel):
    document_id: int
    user_id: int
    org_id: Optional[int] = None
    # token_identifier: str
    is_human: bool
    text: str


class ChatUpdate(BaseModel):
    token_identifier: Optional[str] = None
    is_human: Optional[bool] = None
    text: Optional[str] = None


class ChatResponse(BaseModel):
    meta: MetaResponse
    data: ChatData


class ChatsResponse(BaseModel):
    meta: MetaResponse
    data: List[ChatData]
