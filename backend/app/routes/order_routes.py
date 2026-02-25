from app.config.dependency import get_current_admin_user, get_current_user
from app.database.models.models import User
from fastapi import APIRouter, HTTPException, status, Depends
from app.config.database import get_db
from app.database.schemas.orders_schema import OrderCreate, OrderResponse, OrderUpdate
from app.services.order_service import OrderService
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.order_validation import validate_order_data

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Not authorized"},
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)

@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends()
):
    """Get all orders (admin only)"""
    return await order_service.get_all_orders(db)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends()
):
    """Get order by ID (admin only)"""
    order = await order_service.get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order

@router.post("/place-order", response_model=dict)
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends()
):
    """Create a new order"""
    # Validate order data
    is_valid, error_message = validate_order_data(order.model_dump())
    if not is_valid:
        raise HTTPException(status_code=400, detail=error_message)
    
    # Ensure the user is creating an order for themselves
    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create orders for yourself"
        )
    
    return await order_service.create_order(db, order, order.user_id)

@router.get("/user/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    order_service: OrderService = Depends()
):
    """Get all orders for a user"""
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these orders"
        )
    return await order_service.get_user_orders(db, user_id)

@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: UUID,
    order: OrderUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends()
):
    """Update an order (admin only)"""
    updated_order = await order_service.update_order(db, order_id, order)
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return updated_order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends()
):
    """Delete an order (admin only)"""
    deleted = await order_service.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return None

@router.get("/product/{product_id}", response_model=List[OrderResponse])
async def get_product_orders(
    product_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
    order_service: OrderService = Depends()
):
    """Get all orders for a product (admin only)"""
    return await order_service.get_product_orders(db, product_id)
