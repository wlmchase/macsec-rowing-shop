from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from ..models.models import Order, OrderItem, Product, ShippingInfo, PaymentInfo
from ..schemas.orders_schema import OrderCreate, OrderUpdate
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload
import logging

# Configure logging
logger = logging.getLogger(__name__)

### ORDERS ###
async def create_order(db: AsyncSession, order: OrderCreate) -> Order:
    """Create a new order with its items and update product stock."""
    logger.debug("Starting create_order in repository")
    # First check if all products have enough stock and calculate total price
    total_price = 0
    products_to_update = []
    
    logger.debug("Validating products and calculating total price")
    for item in order.items:
        logger.debug(f"Processing item with product_id: {item.product_id}")
        stmt = select(Product).filter(Product.id == item.product_id)
        result = await db.execute(stmt)
        product = result.scalar_one_or_none()
        
        if not product:
            logger.error(f"Product not found: {item.product_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )
            
        if product.stock < item.quantity:
            logger.error(f"Insufficient stock for product {product.name}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product {product.name}. Available: {product.stock}, Requested: {item.quantity}"
            )
            
        # Calculate item total and add to order total
        if item.quantity < 1:
            logger.error(f"Invalid quantity for product {product.name}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid quantity for product {product.name}. Quantity must be at least 1."
            )
            
        if product.price <= 0:
            logger.error(f"Invalid price for product {product.name}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Invalid price for product {product.name}. Price must be greater than 0."
            )
        item_total = product.price * item.quantity
        total_price += item_total
        
        # Store product info for later update
        products_to_update.append((product, item.quantity))
        logger.debug(f"Added product {product.name} to update list")

    try:
        logger.debug("Creating order with total price: %s", total_price)
        # Create the order with calculated total price
        db_order = Order(user_id=order.user_id, total_price=total_price)
        db.add(db_order)
        logger.debug("Flushing order to get ID")
        await db.flush()
        
        # Create shipping info if provided
        if order.shippingDetails:
            logger.debug("Creating shipping info")
            shipping_info = ShippingInfo(
                order_id=db_order.id,
                first_name=order.shippingDetails.firstName,
                last_name=order.shippingDetails.lastName,
                email=order.shippingDetails.email,
                address=order.shippingDetails.address,
                unit=order.shippingDetails.unit,
                city=order.shippingDetails.city,
                province=order.shippingDetails.province,
                zip_code=order.shippingDetails.zip_code,
                country=order.shippingDetails.country
            )
            db.add(shipping_info)

        # Create payment info if provided
        if order.paymentDetails:
            logger.debug("Creating payment info")
            payment_info = PaymentInfo(
                order_id=db_order.id,
                card_number=order.paymentDetails.cardNumber,
                card_holder=f"{order.shippingDetails.firstName} {order.shippingDetails.lastName}",
                expiration_date=order.paymentDetails.expiryDate,
                cvv=order.paymentDetails.cvv
            )
            db.add(payment_info)
        
        # Create order items and update product stock
        logger.debug("Creating order items and updating product stock")
        for (product, quantity) in products_to_update:
            # Create order item
            db_order_item = OrderItem(
                order_id=db_order.id,
                product_id=product.id,
                quantity=quantity
            )
            db.add(db_order_item)
            
            # Update product stock
            stmt = (
                update(Product)
                .where(Product.id == product.id)
                .values(stock=Product.stock - quantity)
                .returning(Product)
            )
            await db.execute(stmt)
        
        # Get the complete order with all relationships before committing
        logger.debug("Fetching complete order with relationships")
        stmt = (
            select(Order)
            .options(
                selectinload(Order.items).selectinload(OrderItem.product),
                selectinload(Order.shipping_info),
                selectinload(Order.payment_info)
            )
            .filter(Order.id == db_order.id)
        )
        result = await db.execute(stmt)
        complete_order = result.scalar_one()
        logger.debug("Successfully fetched complete order")
        
        # Now commit the transaction
        logger.debug("Committing transaction")
        await db.commit()
        
        return complete_order
    except Exception as e:
        logger.error("Error in create_order: %s", str(e), exc_info=True)
        await db.rollback()
        raise

async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Get all orders with pagination."""
    stmt = (
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.shipping_info)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_order_by_id(db: AsyncSession, order_id: UUID):
    """Get a specific order by ID."""
    stmt = (
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.shipping_info),
            selectinload(Order.payment_info)
        )
        .filter(Order.id == order_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_user_orders(db: AsyncSession, user_id: UUID):
    """Get all orders for a specific user."""
    stmt = (
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.shipping_info)
        )
        .filter(Order.user_id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_order(db: AsyncSession, order_id: UUID, order_update: OrderUpdate):
    """Update an order's details."""
    stmt = (
        update(Order)
        .where(Order.id == order_id)
        .values(**order_update.model_dump(exclude_unset=True))
        .returning(Order)
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.scalar_one_or_none()

async def delete_order(db: AsyncSession, order_id: UUID) -> bool:
    """Delete an order and its items."""
    # First delete related order items
    await db.execute(delete(OrderItem).where(OrderItem.order_id == order_id))
    
    # Delete shipping info
    await db.execute(delete(ShippingInfo).where(ShippingInfo.order_id == order_id))
    
    # Then delete the order
    stmt = delete(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0

async def get_product_orders(db: AsyncSession, product_id: UUID):
    """Get all orders containing a specific product."""
    stmt = (
        select(Order)
        .join(OrderItem)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.shipping_info)
        )
        .filter(OrderItem.product_id == product_id)
        .distinct()
    )
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_all_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Get all orders with pagination."""
    return await get_orders(db, skip, limit)
