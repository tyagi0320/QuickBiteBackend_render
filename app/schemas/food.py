# app/schemas/food.py
from pydantic import BaseModel
from typing import Optional

class FoodBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None

class FoodCreate(FoodBase):
    pass

class FoodUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None

class FoodResponse(FoodBase):
    id: int

    class Config:
        from_attribute = True
