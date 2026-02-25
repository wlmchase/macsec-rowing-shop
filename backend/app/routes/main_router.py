from fastapi import APIRouter
from app.routes import user_routes
from app.routes import auth_routes, contact_routes, order_routes, product_routes

api_router = APIRouter()
api_router.include_router(contact_routes.router)
api_router.include_router(order_routes.router)
api_router.include_router(product_routes.router)
api_router.include_router(user_routes.router)
api_router.include_router(auth_routes.router)