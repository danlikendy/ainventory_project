from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

# Базовые схемы
class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None

# Схемы для складов
class WarehouseBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=200)
    capacity: Optional[float] = Field(None, ge=0)

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseUpdate(WarehouseBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class WarehouseResponse(WarehouseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Схемы для категорий
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class CategoryResponse(BaseModel):
    id: int
    created_at: datetime
    children: List['CategoryResponse'] = []

    class Config:
        from_attributes = True

# Схемы для брендов
class BrandBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    website: Optional[str] = Field(None, max_length=200)

class BrandCreate(BrandBase):
    pass

class BrandUpdate(BrandBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class BrandResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Схемы для продуктов
class ProductBase(BaseModel):
    sku: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    unit_cost: Optional[float] = Field(None, ge=0)
    unit_price: Optional[float] = Field(None, ge=0)
    weight: Optional[float] = Field(None, ge=0)
    dimensions: Optional[str] = Field(None, max_length=100)
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    name: Optional[str] = Field(None, min_length=1, max_length=200)

class ProductResponse(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    category: Optional[CategoryResponse] = None
    brand: Optional[BrandResponse] = None

    class Config:
        from_attributes = True

# Схемы для инвентаря
class InventoryItemBase(BaseModel):
    product_id: int
    warehouse_id: int
    current_stock: float = Field(default=0, ge=0)
    min_stock: float = Field(default=0, ge=0)
    max_stock: float = Field(default=0, ge=0)
    reorder_point: float = Field(default=0, ge=0)
    safety_stock: float = Field(default=0, ge=0)
    lead_time_days: int = Field(default=0, ge=0)

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(InventoryItemBase):
    product_id: Optional[int] = None
    warehouse_id: Optional[int] = None

class InventoryItemResponse(BaseModel):
    id: int
    last_updated: Optional[datetime]
    created_at: datetime
    product: ProductResponse
    warehouse: WarehouseResponse

    class Config:
        from_attributes = True

# Схемы для продаж
class SaleBase(BaseModel):
    product_id: int
    warehouse_id: int
    sale_date: datetime
    quantity: float = Field(..., gt=0)
    revenue: float = Field(..., gt=0)
    cost: Optional[float] = Field(None, ge=0)
    customer_id: Optional[str] = Field(None, max_length=100)
    transaction_id: Optional[str] = Field(None, max_length=100)

class SaleCreate(SaleBase):
    pass

class SaleUpdate(SaleBase):
    product_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    sale_date: Optional[datetime] = None
    quantity: Optional[float] = Field(None, gt=0)
    revenue: Optional[float] = Field(None, gt=0)

class SaleResponse(BaseModel):
    id: int
    created_at: datetime
    product: ProductResponse
    warehouse: WarehouseResponse

    class Config:
        from_attributes = True

# Схемы для прогнозов
class ForecastBase(BaseModel):
    product_id: int
    warehouse_id: int
    forecast_date: datetime
    forecast_value: float = Field(..., ge=0)
    confidence_lower: Optional[float] = Field(None, ge=0)
    confidence_upper: Optional[float] = Field(None, ge=0)
    model_name: str = Field(..., min_length=1, max_length=100)
    model_version: Optional[str] = Field(None, max_length=50)
    features_used: Optional[str] = None
    accuracy_metrics: Optional[str] = None

class ForecastCreate(ForecastBase):
    pass

class ForecastUpdate(ForecastBase):
    product_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    forecast_date: Optional[datetime] = None
    forecast_value: Optional[float] = Field(None, ge=0)

class ForecastResponse(BaseModel):
    id: int
    created_at: datetime
    product: ProductResponse

    class Config:
        from_attributes = True

# Схемы для загрузки данных
class DataUploadBase(BaseModel):
    filename: str
    file_path: str
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    status: str = "uploaded"
    records_processed: int = 0
    error_message: Optional[str] = None
    processed_by: Optional[str] = None

class DataUploadCreate(DataUploadBase):
    pass

class DataUploadUpdate(DataUploadBase):
    filename: Optional[str] = None
    file_path: Optional[str] = None

class DataUploadResponse(BaseModel):
    id: int
    upload_date: datetime

    class Config:
        from_attributes = True

# Схемы для анализа
class InventoryAnalytics(BaseModel):
    total_products: int
    low_stock_items: int
    out_of_stock_items: int
    total_value: float
    average_turnover: float

class SalesAnalytics(BaseModel):
    total_sales: int
    total_revenue: float
    total_quantity: float
    average_order_value: float
    top_products: List[Dict[str, Any]]

class ForecastAnalytics(BaseModel):
    total_forecasts: int
    average_accuracy: float
    models_used: List[str]
    next_forecast_date: Optional[datetime]

# Схемы для загрузки файлов
class FileUploadRequest(BaseModel):
    file_type: str = Field(..., description="Тип данных в файле: sales, inventory, products")
    warehouse_id: Optional[int] = None
    category_id: Optional[int] = None

class FileUploadResponse(BaseModel):
    success: bool
    message: str
    records_processed: int
    errors: List[str] = []
    file_id: Optional[int] = None

# Схемы для поиска и фильтрации
class SearchParams(BaseModel):
    query: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    warehouse_id: Optional[int] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock: Optional[bool] = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int

# Обновляем forward references
CategoryResponse.model_rebuild()
ProductResponse.model_rebuild()
InventoryItemResponse.model_rebuild()
SaleResponse.model_rebuild()
ForecastResponse.model_rebuild()
