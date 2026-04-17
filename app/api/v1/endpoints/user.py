from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User  
from app.schemas.user import UserResponse
from app.dependencies.auth import get_current_user,admin_only

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db), 
    admin = Depends(admin_only)
):
    return db.query(User).all()


@router.get("/me", response_model=UserResponse)
def get_me(
    db: Session = Depends(get_db), 
    current_user_info = Depends(get_current_user)
):
    user_id = current_user_info.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found in database")
        
    return user
