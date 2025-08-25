from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

Base = declarative_base()

class Warehouse(Base):
    __tablename__ = "warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    location = Column(String(200))
    capacity = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    inventory_items = relationship("InventoryItem", back_populates="warehouse")
    sales = relationship("Sale", back_populates="warehouse")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    products = relationship("Product", back_populates="category")
    children = relationship("Category")

class Brand(Base):
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    website = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    products = relationship("Product", back_populates="brand")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), nullable=False, unique=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id"))
    brand_id = Column(Integer, ForeignKey("brands.id"))
    unit_cost = Column(Float)
    unit_price = Column(Float)
    weight = Column(Float)
    dimensions = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Связи
    category = relationship("Category", back_populates="products")
    brand = relationship("Brand", back_populates="products")
    inventory_items = relationship("InventoryItem", back_populates="product")
    sales = relationship("Sale", back_populates="product")
    forecasts = relationship("Forecast", back_populates="product")
    
    # Индексы
    __table_args__ = (
        Index('idx_product_sku', 'sku'),
        Index('idx_product_category', 'category_id'),
        Index('idx_product_brand', 'brand_id'),
    )

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    current_stock = Column(Float, default=0)
    min_stock = Column(Float, default=0)
    max_stock = Column(Float, default=0)
    reorder_point = Column(Float, default=0)
    safety_stock = Column(Float, default=0)
    lead_time_days = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    product = relationship("Product", back_populates="inventory_items")
    warehouse = relationship("Warehouse", back_populates="inventory_items")
    
    # Индексы
    __table_args__ = (
        Index('idx_inventory_product_warehouse', 'product_id', 'warehouse_id'),
        Index('idx_inventory_current_stock', 'current_stock'),
    )

class Sale(Base):
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    sale_date = Column(DateTime(timezone=True), nullable=False)
    quantity = Column(Float, nullable=False)
    revenue = Column(Float, nullable=False)
    cost = Column(Float)
    customer_id = Column(String(100))
    transaction_id = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    product = relationship("Product", back_populates="sales")
    warehouse = relationship("Warehouse", back_populates="sales")
    
    # Индексы
    __table_args__ = (
        Index('idx_sale_date', 'sale_date'),
        Index('idx_sale_product_date', 'product_id', 'sale_date'),
        Index('idx_sale_warehouse_date', 'warehouse_id', 'sale_date'),
    )

class Forecast(Base):
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    forecast_date = Column(DateTime(timezone=True), nullable=False)
    forecast_value = Column(Float, nullable=False)
    confidence_lower = Column(Float)
    confidence_upper = Column(Float)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(50))
    features_used = Column(Text)  # JSON string
    accuracy_metrics = Column(Text)  # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    product = relationship("Product", back_populates="forecasts")
    
    # Индексы
    __table_args__ = (
        Index('idx_forecast_product_date', 'product_id', 'forecast_date'),
        Index('idx_forecast_warehouse_date', 'warehouse_id', 'forecast_date'),
        Index('idx_forecast_model', 'model_name'),
    )

class DataUpload(Base):
    __tablename__ = "data_uploads"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer)
    file_type = Column(String(100))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="uploaded")  # uploaded, processing, completed, failed
    records_processed = Column(Integer, default=0)
    error_message = Column(Text)
    processed_by = Column(String(100))
    
    # Индексы
    __table_args__ = (
        Index('idx_upload_status', 'status'),
        Index('idx_upload_date', 'upload_date'),
    )
