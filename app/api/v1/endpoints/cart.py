from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.cart import Cart
from app.schemas.cart import CartCreate, CartResponse
from app.dependencies.auth import user_only
from fastapi.security import HTTPBearer

router = APIRouter(prefix="/cart", tags=["Cart"],dependencies=[Depends(HTTPBearer())])

@router.post("/add", response_model=CartResponse)
def add_to_cart(
    data: CartCreate,
    db: Session = Depends(get_db),
    current_user=Depends(user_only)
):
    cart_item = db.query(Cart).filter(
        Cart.user_id == current_user["user_id"],
        Cart.food_id == data.food_id
    ).first()
 
    if cart_item:
        cart_item.quantity += data.quantity
    else:
        cart_item = Cart(
            user_id=current_user["user_id"],
            food_id=data.food_id,
            quantity=data.quantity
        )
        db.add(cart_item)
 
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.put("/{cart_id}", response_model=CartResponse)
def update_cart_quantity(
    cart_id: int,
    quantity: int, 
    db: Session = Depends(get_db),
    current_user = Depends(user_only)
):
    cart_item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == current_user["user_id"]
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.get("/", response_model=list[CartResponse])
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(user_only)
):
    # This ensures User 2 only ever sees User 2's data
    return db.query(Cart).filter(Cart.user_id == current_user["user_id"]).all()
 
@router.delete("/{cart_id}")
def remove_from_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(user_only)
):
    item = db.query(Cart).filter(
        Cart.id == cart_id,
        Cart.user_id == current_user["user_id"]
    ).first()
 
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
 
    db.delete(item)
    db.commit()
    return {"message": "Item removed"}
