from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from app.config.database import Base
import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID


class Role(enum.Enum):
    ADMIN = 42
    USER = 33

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Role), default=Role.USER)
    is_active = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="user")

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    def dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_admin": self.is_admin,
            "is_active": self.is_active
        }

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), index=True)
    description = Column(String(500))
    price = Column(Float)
    stock = Column(Integer)

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.now(timezone.utc))
    total_price = Column(Float(precision=2, asdecimal=True), nullable=False)
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")
    shipping_info = relationship("ShippingInfo", back_populates="order", uselist=False)
    payment_info = relationship("PaymentInfo", back_populates="order", uselist=False)

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    quantity = Column(Integer)
    order = relationship("Order", back_populates="items")
    product = relationship("Product")


class ShippingInfo(Base):
    __tablename__ = "shipping_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    address = Column(String)
    unit = Column(String, nullable=True)
    city = Column(String)
    province = Column(String)
    zip_code = Column(String, nullable=False)
    country = Column(String)
    order = relationship("Order", back_populates="shipping_info")

# class BillingInfo(Base):
#     __tablename__ = "billing_info"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
#     order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), unique=True)
#     address = Column(String)
#     unit = Column(String, nullable=True)
#     city = Column(String)
#     province = Column(String)
#     zipcode = Column(String)
#     country = Column(String)
#     order = relationship("Order", back_populates="billing_info")

class PaymentInfo(Base):
    __tablename__ = "payment_info"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), unique=True)
    card_number = Column(String)
    card_holder = Column(String)
    expiration_date = Column(String)
    cvv = Column(String)
    order = relationship("Order", back_populates="payment_info")

class ContactForm(Base):
    __tablename__ = "contact_form"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(100), index=True)
    message = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = Column(String, unique=True, index=True)
    blacklisted_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True))
