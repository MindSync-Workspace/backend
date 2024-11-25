from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MembershipCreate(BaseModel):
    user_id: int
    membership_type: str
    start_date: datetime
    end_date: datetime

class MembershipUpdate(BaseModel):
    membership_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class MembershipResponse(BaseModel):
    id: int
    user_id: int
    membership_type: str
    start_date: datetime
    end_date: datetime
    created_at: datetime
    modified_at: datetime
