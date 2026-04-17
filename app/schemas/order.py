from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime

# Represents an item within an order (Snapshot of food at time of purchase)
# Useful if you plan to implement an OrderItems table later
class OrderItemResponse(BaseModel):
    food_id: int
    quantity: int
    price_at_purchase: float 

    class Config:
        from_attributes = True

# Main Order Response (What the User and Admin see)
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: Literal["pending", "approved", "delivered"] = "pending"
    # If your SQLAlchemy model has a created_at field, uncomment below:
    # created_at: datetime 

    class Config:
        from_attributes = True

class OrderUpdateStatus(BaseModel):
    # This ensures the Admin can only send these 3 specific strings
    status: Literal["pending", "approved", "delivered"]

class OrderCreate(BaseModel):
    pass
