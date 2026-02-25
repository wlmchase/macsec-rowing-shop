from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database.repository.order_repo import (
    create_order,
    get_orders,
    get_order_by_id,
    get_user_orders,
    update_order,
    delete_order,
    get_product_orders
)
from app.database.schemas.orders_schema import OrderCreate, OrderResponse, OrderUpdate
from app.database.models.models import Order, OrderItem
from uuid import UUID
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class OrderService:
    async def create_order(self, db: AsyncSession, order: OrderCreate, user_id: UUID) -> dict:
        """Create a new order"""
        logger.debug(f"Starting create_order in OrderService for user_id: {user_id}")
        try:
            order.user_id = user_id
            if order.user_id != user_id:
                logger.error(f"Authentication failure: user_id mismatch")
                return {
                    "success": False,
                    "message": "Authentication failure: user_id mismatch",
                    "data": None
                }
            
            logger.debug("Calling create_order in repository")
            # Create the order and get it back with all relationships loaded
            db_order = await create_order(db, order)
            logger.debug("Successfully created order in repository")

            return {
                "success": True,
                "message": "Order created successfully"
            }
        except Exception as e:
            logger.error(f"Error in create_order: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"Failed to create order: {str(e)}"
            }

    async def get_user_orders(self, db: AsyncSession, user_id: UUID) -> list[OrderResponse]:
        """Get all orders for a user"""
        orders = await get_user_orders(db, user_id)
        return [OrderResponse.model_validate(order) for order in orders]

    async def get_order(self, db: AsyncSession, order_id: UUID) -> OrderResponse:
        """Get order by ID"""
        order = await get_order_by_id(db, order_id)
        if not order:
            return None
        return OrderResponse.model_validate(order)

    async def get_all_orders(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[OrderResponse]:
        """Get all orders with pagination"""
        orders = await get_orders(db, skip, limit)
        return [OrderResponse.from_orm(order) for order in orders]

    async def get_order_by_id(self, db: AsyncSession, order_id: UUID) -> OrderResponse | None:
        """Get order by ID"""
        order = await get_order_by_id(db, order_id)
        if not order:
            return None
        return OrderResponse.model_validate(order)

    async def update_order(self, db: AsyncSession, order_id: UUID, order: OrderUpdate) -> OrderResponse | None:
        """Update an order"""
        updated_order = await update_order(db, order_id, order)
        if not updated_order:
            return None
        return OrderResponse.model_validate(updated_order)

    async def delete_order(self, db: AsyncSession, order_id: UUID) -> bool:
        """Delete an order"""
        return await delete_order(db, order_id)

    async def get_product_orders(self, db: AsyncSession, product_id: UUID) -> list[OrderResponse]:
        """Get all orders containing a specific product"""
        orders = await get_product_orders(db, product_id)
        return [OrderResponse.model_validate(order) for order in orders]