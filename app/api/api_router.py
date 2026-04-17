# api/v1/api_router.py
from fastapi import APIRouter
from app.api.v1.endpoints import auth,food,cart,order,user

api_router = APIRouter()


api_router.include_router(auth.router)
api_router.include_router(user.router)
api_router.include_router(food.router)
api_router.include_router(cart.router)
api_router.include_router(order.router)

