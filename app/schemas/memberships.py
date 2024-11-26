from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MembershipCreate(BaseModel):
    user_id: int
    org_id: int


class MembershipUpdate(BaseModel):
    user_id: int
    org_id: int


class MembershipResponse(BaseModel):
    id: int
    user_id: int
    org_id: int
    created_at: datetime
    modified_at: datetime
