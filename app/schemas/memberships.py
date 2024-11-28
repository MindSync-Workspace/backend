from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MetaResponse(BaseModel):
    status: int
    message: str


class MembershipData(BaseModel):
    id: int
    user_id: int
    org_id: int
    created_at: datetime
    modified_at: datetime


class MembershipCreate(BaseModel):
    user_id: int
    org_id: int


class MembershipUpdate(BaseModel):
    user_id: int
    org_id: int


class MembershipResponse(BaseModel):
    meta: MetaResponse
    data: MembershipData


class MembershipsResponse(BaseModel):
    meta: MetaResponse
    data: List[MembershipData]
