from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.package import Package
from typing import Dict, Any
import csv
import io

router = APIRouter()


@router.get("/packages.csv")
async def packages_csv_report(db: Session = Depends(get_db)):
    """Generate CSV report of packages"""
    packages = db.query(Package).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "Tracking ID", "Sender Name", "Sender Phone", 
        "Receiver Name", "Receiver Phone", "Status", 
        "Created At", "Updated At"
    ])
    
    for pkg in packages:
        writer.writerow([
            pkg.tracking_id,
            pkg.sender_name,
            pkg.sender_phone,
            pkg.receiver_name,
            pkg.receiver_phone,
            pkg.status,
            pkg.created_at.isoformat(),
            pkg.updated_at.isoformat() if pkg.updated_at else ""
        ])
    
    output.seek(0)
    
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=packages_report.csv"}
    )


@router.get("/warehouse-stats")
async def warehouse_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get warehouse statistics"""
    return {
        "total_packages": db.query(Package).count(),
        "by_status": {
            "registered": db.query(Package).filter(Package.status == "registered").count(),
            "in_transit": db.query(Package).filter(Package.status == "in_transit").count(),
            "delivered": db.query(Package).filter(Package.status == "delivered").count(),
        }
    }
