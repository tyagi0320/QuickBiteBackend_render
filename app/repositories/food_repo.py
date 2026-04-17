# # app/crud/food.py
# from sqlalchemy.orm import Session
# from app.models.food import Food
# from app.schemas.food import FoodCreate, FoodUpdate


# def create_food_with_image(
#     db: Session,
#     name: str,
#     description: str,
#     price: float,
#     image_path: str
# ):
#     food = Food(
#         name=name,
#         description=description,
#         price=price,
#         image=image_path
#     )
#     db.add(food)
#     db.commit()
#     db.refresh(food)
#     return food


# def get_food(db: Session, food_id: int):
#     return db.query(Food).filter(Food.id == food_id).first()

# def get_all_foods(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Food).offset(skip).limit(limit).all()

# def update_food(db: Session, food_id: int, food: FoodUpdate):
#     db_food = get_food(db, food_id)
#     if not db_food:
#         return None

#     for key, value in food.dict(exclude_unset=True).items():
#         setattr(db_food, key, value)

#     db.commit()
#     db.refresh(db_food)
#     return db_food

# def delete_food(db: Session, food_id: int):
#     db_food = get_food(db, food_id)
#     if not db_food:
#         return None

#     db.delete(db_food)
#     db.commit()
#     return db_food

from sqlalchemy.orm import Session
from app.models.food import Food

def create_food_with_image(db: Session, name: str, description: str, price: float, image_path: str):
    food = Food(name=name, description=description, price=price, image=image_path)
    db.add(food)
    db.commit()
    db.refresh(food)
    return food

def get_food(db: Session, food_id: int):
    return db.query(Food).filter(Food.id == food_id).first()

def get_all_foods(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Food).offset(skip).limit(limit).all()

def update_food_data(db: Session, food_id: int, update_data: dict):
    db_food = get_food(db, food_id)
    if not db_food:
        return None

    for key, value in update_data.items():
        setattr(db_food, key, value)

    db.commit()
    db.refresh(db_food)
    return db_food

def delete_food(db: Session, food_id: int):
    db_food = get_food(db, food_id)
    if not db_food:
        return None

    db.delete(db_food)
    db.commit()
    return db_food
