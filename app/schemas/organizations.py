from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrganizationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class OrganizationResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    modified_at: datetime
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
