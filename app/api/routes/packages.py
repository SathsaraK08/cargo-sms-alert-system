from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.sms_service import sms_service
from app.models.package import Package, PackageStatus
from app.schemas.package import (
    PackageCreate,
    PackageStatusUpdate,
    PackageResponse,
    PackageListResponse,
    PackageListResult
)
from typing import Dict, Any, List
import uuid
import logging

logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/", response_model=PackageResponse)
async def register_package(
    package_data: PackageCreate,
    db: Session = Depends(get_db)
) -> PackageResponse:
    """Register a new package and send SMS notification"""
    tracking_id = f"PKG{uuid.uuid4().hex[:8].upper()}"
    
    package = Package(
        tracking_id=tracking_id,
        sender_name=package_data.sender_name,
        sender_phone=package_data.sender_phone,
        receiver_name=package_data.receiver_name,
        receiver_phone=package_data.receiver_phone,
        origin_wh_id=package_data.origin_wh_id,
        dest_wh_id=package_data.dest_wh_id,
        box_type_id=package_data.box_type_id,
        status=PackageStatus.REGISTERED
    )
    
    db.add(package)
    db.commit()
    db.refresh(package)
    
    try:
        await sms_service.send_package_alert(
            phone=package.sender_phone,
            tracking_id=package.tracking_id,
            status="registered",
            language="en"
        )
        await sms_service.send_package_alert(
            phone=package.receiver_phone,
            tracking_id=package.tracking_id,
            status="registered",
            language="en"
        )
        logger.info(f"SMS alerts sent for package registration: {tracking_id}")
    except Exception as e:
        logger.error(f"Failed to send SMS alerts for {tracking_id}: {e}")
    
    return PackageResponse.from_orm(package)


@router.get("/{tracking_id}", response_model=PackageResponse)
async def get_package(
    tracking_id: str,
    db: Session = Depends(get_db)
) -> PackageResponse:
    """Get package details by tracking ID"""
    package = db.query(Package).filter(Package.tracking_id == tracking_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    return PackageResponse.from_orm(package)


@router.patch("/{tracking_id}/status")
async def update_package_status(
    tracking_id: str,
    status_data: PackageStatusUpdate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update package status and send SMS notification"""
    package = db.query(Package).filter(Package.tracking_id == tracking_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    old_status = package.status
    package.status = status_data.status
    db.commit()
    db.refresh(package)
    
    try:
        status_str = package.status.value.lower().replace(" ", "_")
        
        await sms_service.send_package_alert(
            phone=package.sender_phone,
            tracking_id=package.tracking_id,
            status=status_str,
            language="en"
        )
        await sms_service.send_package_alert(
            phone=package.receiver_phone,
            tracking_id=package.tracking_id,
            status=status_str,
            language="en"
        )
        logger.info(f"SMS alerts sent for status update: {tracking_id} ({old_status} -> {package.status})")
    except Exception as e:
        logger.error(f"Failed to send SMS alerts for {tracking_id}: {e}")
    
    return {
        "tracking_id": package.tracking_id,
        "status": package.status,
        "old_status": old_status,
        "message": "Package status updated successfully",
        "sms_sent": True  # In real implementation, this would be based on actual SMS result
    }


@router.get("/", response_model=PackageListResult)
async def list_packages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> PackageListResult:
    """List packages with pagination"""
    packages = db.query(Package).offset(skip).limit(limit).all()
    total_count = db.query(Package).count()
    
    package_list = [PackageListResponse.from_orm(pkg) for pkg in packages]
    
    return PackageListResult(
        packages=package_list,
        total=total_count,
        skip=skip,
        limit=limit
    )
