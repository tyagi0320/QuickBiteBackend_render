from pydantic import BaseModel
 
class CartCreate(BaseModel):
    food_id: int
    quantity: int = 1
 
class CartResponse(BaseModel):
    id: int
    food_id: int
    quantity: int
 
    class Config:
        from_attributes = True