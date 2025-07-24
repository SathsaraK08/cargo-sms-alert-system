from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.package import Package, PackageStatus
from typing import Dict, Any, List
import uuid

router = APIRouter()


@router.post("/")
async def register_package(
    package_data: Dict[str, Any],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Register a new package"""
    tracking_id = f"PKG{uuid.uuid4().hex[:8].upper()}"
    
    package = Package(
        tracking_id=tracking_id,
        sender_name=package_data["sender_name"],
        sender_phone=package_data["sender_phone"],
        receiver_name=package_data["receiver_name"],
        receiver_phone=package_data["receiver_phone"],
        origin_wh_id=package_data["origin_wh_id"],
        dest_wh_id=package_data["dest_wh_id"],
        box_type_id=package_data["box_type_id"],
        status=PackageStatus.REGISTERED
    )
    
    db.add(package)
    db.commit()
    db.refresh(package)
    
    return {
        "id": str(package.id),
        "tracking_id": package.tracking_id,
        "status": package.status,
        "message": "Package registered successfully"
    }


@router.get("/{tracking_id}")
async def get_package(
    tracking_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get package details by tracking ID"""
    package = db.query(Package).filter(Package.tracking_id == tracking_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    return {
        "id": str(package.id),
        "tracking_id": package.tracking_id,
        "sender_name": package.sender_name,
        "sender_phone": package.sender_phone,
        "receiver_name": package.receiver_name,
        "receiver_phone": package.receiver_phone,
        "status": package.status,
        "created_at": package.created_at.isoformat(),
        "updated_at": package.updated_at.isoformat() if package.updated_at else None
    }


@router.patch("/{tracking_id}/status")
async def update_package_status(
    tracking_id: str,
    status_data: Dict[str, str],
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Update package status"""
    package = db.query(Package).filter(Package.tracking_id == tracking_id).first()
    
    if not package:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Package not found"
        )
    
    new_status = status_data.get("status")
    if new_status not in [status.value for status in PackageStatus]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status"
        )
    
    package.status = PackageStatus(new_status)
    db.commit()
    db.refresh(package)
    
    return {
        "tracking_id": package.tracking_id,
        "status": package.status,
        "message": "Package status updated successfully"
    }


@router.get("/")
async def list_packages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """List packages with pagination"""
    packages = db.query(Package).offset(skip).limit(limit).all()
    
    return {
        "packages": [
            {
                "id": str(pkg.id),
                "tracking_id": pkg.tracking_id,
                "sender_name": pkg.sender_name,
                "receiver_name": pkg.receiver_name,
                "status": pkg.status,
                "created_at": pkg.created_at.isoformat()
            }
            for pkg in packages
        ],
        "total": len(packages)
    }
