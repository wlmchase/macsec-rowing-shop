from pydantic import BaseModel, UUID4, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re

class OrderItemBase(BaseModel):
    product_id: UUID4
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class ProductResponse(BaseModel):
    id: UUID4
    name: str
    price: float
    stock: int
    description: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True

class OrderItemResponse(OrderItemBase):
    id: UUID4
    product: ProductResponse
    price: float | None = None

    class Config:
        from_attributes = True

class ShippingDetails(BaseModel):
    firstName: str
    lastName: str
    email: str
    address: str
    city: str
    province: str
    zip_code: str
    unit: Optional[str] = None
    country: str = "CAN"  # Default to Canada if not provided

class PaymentDetails(BaseModel):
    cardNumber: str = Field(..., min_length=15, max_length=16)
    expiryDate: str  # Format: MM/YY
    cvv: str = Field(..., min_length=3, max_length=3)

    @field_validator('cardNumber')
    def validate_card_number(cls, v):
        if not v.isdigit():
            raise ValueError('Card number must contain only digits')
        if len(v) not in [15, 16]:
            raise ValueError('Card number must be 15 or 16 digits')
        return v

    @field_validator('expiryDate')
    def validate_expiry_date(cls, v):
        # Check format
        if not re.match(r'^(0[1-9]|1[0-2])/[0-9]{2}$', v):
            raise ValueError('Expiry date must be in MM/YY format')
        
        # Check if expired
        month, year = map(int, v.split('/'))
        expiry_date = datetime(2000 + year, month, 1)  # First day of expiry month
        if expiry_date < datetime.now():
            raise ValueError('Card has expired')
        return v

    @field_validator('cvv')
    def validate_cvv(cls, v):
        if not v.isdigit():
            raise ValueError('CVV must contain only digits')
        if len(v) != 3:
            raise ValueError('CVV must be exactly 3 digits')
        return v

class OrderBase(BaseModel):
    user_id: UUID4

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]
    shippingDetails: ShippingDetails
    paymentDetails: PaymentDetails

class ShippingInfoResponse(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    email: str
    address: str
    city: str
    province: str
    zip_code: str
    unit: str | None = None
    country: str = "CAN"

    class Config:
        from_attributes = True

class PaymentInfoResponse(BaseModel):
    id: UUID4
    card_number: str
    card_holder: str
    expiration_date: str
    cvv: str

    class Config:
        from_attributes = True

class OrderResponse(OrderBase):
    id: UUID4
    total_price: float
    items: List[OrderItemResponse]
    shipping_info: ShippingInfoResponse
    
    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: str

    class Config:
        from_attributes = True
