from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    iso_code = Column(String(3), unique=True, nullable=False)
    name = Column(String(100), nullable=False)

    warehouses = relationship("Warehouse", back_populates="country")

    def __repr__(self):
        return f"<Country(id={self.id}, iso_code={self.iso_code}, name={self.name})>"


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id"), nullable=False)
    city = Column(String(100), nullable=False)

    country = relationship("Country", back_populates="warehouses")
    origin_packages = relationship("Package", foreign_keys="Package.origin_wh_id", back_populates="origin_warehouse")
    destination_packages = relationship("Package", foreign_keys="Package.dest_wh_id", back_populates="destination_warehouse")

    def __repr__(self):
        return f"<Warehouse(id={self.id}, name={self.name}, city={self.city})>"


class BoxType(Base):
    __tablename__ = "box_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False)
    dim_label = Column(String(100), nullable=False)
    price_lkr = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    packages = relationship("Package", back_populates="box_type")

    def __repr__(self):
        return f"<BoxType(id={self.id}, code={self.code}, price_lkr={self.price_lkr})>"
