from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.filehandler import save_file
from app.core.database import get_db
from app.schemas.food import FoodResponse
from app.repositories.food_repo import (
    create_food_with_image,
    get_food,
    get_all_foods,
    update_food_data,
    delete_food
)

router = APIRouter(prefix="/foods", tags=["Foods"])

# Define allowed image types
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/jpg"]

@router.post("/", response_model=FoodResponse)
def create(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # FIXED: Added the list check here
    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type. Use JPG or PNG.")

    filename = save_file(image)
    return create_food_with_image(db, name, description, price, filename)

@router.get("/", response_model=List[FoodResponse])
def read_all(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_foods(db, skip, limit)

@router.put("/{food_id}", response_model=FoodResponse)
def update(
    food_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    db_food = get_food(db, food_id)
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")

    update_data = {}
    if name is not None: update_data["name"] = name
    if description is not None: update_data["description"] = description
    if price is not None: update_data["price"] = price
    
    if image:
        if image.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(status_code=400, detail="Invalid image type")
        
        update_data["image"] = save_file(image)

    return update_food_data(db, food_id, update_data)

@router.delete("/{food_id}")
def delete(food_id: int, db: Session = Depends(get_db)):
    deleted = delete_food(db, food_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Food not found")
    return {"message": "Food deleted successfully"}
