from pydantic import BaseModel, EmailStr
from datetime import datetime
class UserBase(BaseModel):
    email: EmailStr
    username: str
    created_at: datetime
    user_type: str
    company_name: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProductBase(BaseModel):
    name: str
    category: str
    price: float
    min_quantity: int
    stock: int
    created_at: datetime

class ProductCreate(ProductBase):
    vendor_id: int

class ProductOut(ProductBase):
    id: int
    vendor_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    total_amount: float
    discount_percent: float
    final_amount: float
    created_at: datetime

class OrderCreate(OrderBase):
    buyer_id: int
    product_id: int

class OrderOut(OrderBase):
    id: int
    buyer_id: int
    product_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    quantity: int
    unit_price: float
    subtotal: float
    created_at: datetime

class OrderItemCreate(OrderItemBase):
    order_id: int
    product_id: int

class OrderItemOut(OrderItemBase):
    id: int
    order_id: int
    product_id: int
    created_at: datetime
    class Config:
        from_attributes = True
