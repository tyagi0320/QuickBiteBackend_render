from app.core.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, Float
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    hashed_password = Column(String,nullable=False)
    role = Column(String, nullable=False, server_default="user")
    otp = Column(String, nullable=True)
    otp_expires_at = Column(TIMESTAMP(timezone=True), nullable=True)
    is_verified = Column(Boolean, server_default=text('false'), default=False)    