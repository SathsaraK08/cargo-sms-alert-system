from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Numeric, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum
from app.core.database import Base


class PackageStatus(str, enum.Enum):
    REGISTERED = "registered"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    DELAYED = "delayed"
    CANCELLED = "cancelled"


class Package(Base):
    __tablename__ = "packages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracking_id = Column(String(50), unique=True, nullable=False, index=True)
    sender_name = Column(String(100), nullable=False)
    sender_phone = Column(String(20), nullable=False)
    receiver_name = Column(String(100), nullable=False)
    receiver_phone = Column(String(20), nullable=False)
    origin_wh_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=False)
    dest_wh_id = Column(UUID(as_uuid=True), ForeignKey("warehouses.id"), nullable=False)
    box_type_id = Column(UUID(as_uuid=True), ForeignKey("box_types.id"), nullable=False)
    status = Column(Enum(PackageStatus), nullable=False, default=PackageStatus.REGISTERED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    origin_warehouse = relationship("Warehouse", foreign_keys=[origin_wh_id])
    destination_warehouse = relationship("Warehouse", foreign_keys=[dest_wh_id])
    box_type = relationship("BoxType", back_populates="packages")
    products = relationship("Product", back_populates="package", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Package(id={self.id}, tracking_id={self.tracking_id}, status={self.status})>"


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    package_id = Column(UUID(as_uuid=True), ForeignKey("packages.id"), nullable=False)
    name = Column(String(200), nullable=False)
    qty = Column(Integer, nullable=False, default=1)
    declared_value_lkr = Column(Numeric(12, 2), nullable=False)
    description = Column(Text)

    package = relationship("Package", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, qty={self.qty})>"
