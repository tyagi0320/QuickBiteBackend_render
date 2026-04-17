from app.core.database import Base
from sqlalchemy import Column, Integer, ForeignKey

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    food_id = Column(Integer, ForeignKey("foods.id"), index=True)
    quantity = Column(Integer) 

