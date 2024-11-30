from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MetaResponse(BaseModel):
    status: int
    message: str


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


class OrganizationData(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    modified_at: datetime
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class OrganizationResponse(BaseModel):
    meta: MetaResponse
    data: OrganizationData


class OrganizationsResponse(BaseModel):
    meta: MetaResponse
    data: List[OrganizationData]
