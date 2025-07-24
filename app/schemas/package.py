from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.package import PackageStatus
import uuid


class PackageCreate(BaseModel):
    sender_name: str = Field(..., min_length=1, max_length=100)
    sender_phone: str = Field(..., min_length=10, max_length=20)
    receiver_name: str = Field(..., min_length=1, max_length=100)
    receiver_phone: str = Field(..., min_length=10, max_length=20)
    origin_wh_id: uuid.UUID
    dest_wh_id: uuid.UUID
    box_type_id: uuid.UUID


class PackageStatusUpdate(BaseModel):
    status: PackageStatus


class PackageResponse(BaseModel):
    id: uuid.UUID
    tracking_id: str
    sender_name: str
    sender_phone: str
    receiver_name: str
    receiver_phone: str
    origin_wh_id: uuid.UUID
    dest_wh_id: uuid.UUID
    box_type_id: uuid.UUID
    status: PackageStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PackageListResponse(BaseModel):
    id: uuid.UUID
    tracking_id: str
    sender_name: str
    receiver_name: str
    status: PackageStatus
    created_at: datetime

    class Config:
        from_attributes = True


class PackageListResult(BaseModel):
    packages: list[PackageListResponse]
    total: int
    skip: int
    limit: int
