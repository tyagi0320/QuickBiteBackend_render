from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, text

class Food(Base):
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, nullable=False,index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=False) 
