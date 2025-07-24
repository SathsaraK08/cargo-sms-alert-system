from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_admin, require_staff_or_admin
from app.models.warehouse import BoxType, Warehouse, Country
from app.models.user import User
from typing import Dict, Any, List

router = APIRouter()


@router.get("/boxtypes")
async def list_box_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
) -> Dict[str, Any]:
    """List all box types"""
    box_types = db.query(BoxType).all()
    
    return {
        "box_types": [
            {
                "id": str(bt.id),
                "code": bt.code,
                "dim_label": bt.dim_label,
                "price_lkr": float(bt.price_lkr),
                "created_at": bt.created_at.isoformat(),
                "updated_at": bt.updated_at.isoformat() if bt.updated_at else None
            }
            for bt in box_types
        ]
    }


@router.post("/boxtypes")
async def create_box_type(
    box_type_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
) -> Dict[str, Any]:
    """Create a new box type"""
    box_type = BoxType(
        code=box_type_data["code"],
        dim_label=box_type_data["dim_label"],
        price_lkr=box_type_data["price_lkr"]
    )
    
    db.add(box_type)
    db.commit()
    db.refresh(box_type)
    
    return {
        "id": str(box_type.id),
        "code": box_type.code,
        "dim_label": box_type.dim_label,
        "price_lkr": float(box_type.price_lkr),
        "message": "Box type created successfully"
    }


@router.get("/warehouses")
async def list_warehouses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
) -> Dict[str, Any]:
    """List all warehouses"""
    warehouses = db.query(Warehouse).all()
    
    return {
        "warehouses": [
            {
                "id": str(wh.id),
                "name": wh.name,
                "city": wh.city,
                "country_id": str(wh.country_id)
            }
            for wh in warehouses
        ]
    }


@router.post("/warehouses")
async def create_warehouse(
    warehouse_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
) -> Dict[str, Any]:
    """Create a new warehouse"""
    warehouse = Warehouse(
        name=warehouse_data["name"],
        city=warehouse_data["city"],
        country_id=warehouse_data["country_id"]
    )
    
    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)
    
    return {
        "id": str(warehouse.id),
        "name": warehouse.name,
        "city": warehouse.city,
        "country_id": str(warehouse.country_id),
        "message": "Warehouse created successfully"
    }


@router.get("/countries")
async def list_countries(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_staff_or_admin)
) -> Dict[str, Any]:
    """List all countries"""
    countries = db.query(Country).all()
    
    return {
        "countries": [
            {
                "id": str(country.id),
                "iso_code": country.iso_code,
                "name": country.name
            }
            for country in countries
        ]
    }


@router.post("/countries")
async def create_country(
    country_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
) -> Dict[str, Any]:
    """Create a new country - requires admin role"""
    country = Country(
        iso_code=country_data["iso_code"],
        name=country_data["name"]
    )
    
    db.add(country)
    db.commit()
    db.refresh(country)
    
    return {
        "id": str(country.id),
        "iso_code": country.iso_code,
        "name": country.name,
        "message": "Country created successfully"
    }


@router.get("/users")
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
) -> Dict[str, Any]:
    """List all users - requires admin role"""
    users = db.query(User).all()
    
    return {
        "users": [
            {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "active": user.active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            for user in users
        ]
    }


@router.post("/users")
async def create_user(
    user_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
) -> Dict[str, Any]:
    """Create a new user - requires admin role"""
    from app.core.security import get_password_hash
    
    password = user_data.pop("password")
    user_data["pw_hash"] = get_password_hash(password)
    
    user = User(
        name=user_data["name"],
        email=user_data["email"],
        role=user_data["role"],
        pw_hash=user_data["pw_hash"],
        active=user_data.get("active", True)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "active": user.active,
        "message": "User created successfully"
    }
