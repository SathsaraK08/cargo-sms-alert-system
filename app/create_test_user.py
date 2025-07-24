#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings
import uuid

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_test_users():
    db = SessionLocal()
    try:
        existing_admin = db.query(User).filter(User.email == "admin@test.com").first()
        if existing_admin:
            print("Admin user already exists")
            return
        
        admin_user = User(
            id=uuid.uuid4(),
            name="Test Admin",
            email="admin@test.com",
            role="ADMIN",
            pw_hash=get_password_hash("admin123"),
            active=True
        )
        
        staff_user = User(
            id=uuid.uuid4(),
            name="Test Staff",
            email="staff@test.com",
            role="STAFF",
            pw_hash=get_password_hash("staff123"),
            active=True
        )
        
        viewer_user = User(
            id=uuid.uuid4(),
            name="Test Viewer",
            email="viewer@test.com",
            role="VIEWER",
            pw_hash=get_password_hash("viewer123"),
            active=True
        )
        
        db.add(admin_user)
        db.add(staff_user)
        db.add(viewer_user)
        db.commit()
        
        print("Test users created successfully:")
        print("- Admin: admin@test.com / admin123")
        print("- Staff: staff@test.com / staff123")
        print("- Viewer: viewer@test.com / viewer123")
        
    except Exception as e:
        print(f"Error creating test users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_users()
