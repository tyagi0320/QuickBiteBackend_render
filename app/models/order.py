
from sqlalchemy import Column, Integer, String, ForeignKey, Index, text
from app.core.database import Base 

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    total_price = Column(Integer, server_default="0")
    status = Column(String, index=True, server_default="PENDING")


