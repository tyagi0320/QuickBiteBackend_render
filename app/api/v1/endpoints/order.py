# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from typing import List

# from app.core.database import get_db
# from app.models.order import Order
# from app.models.cart import Cart
# from app.models.food import Food
# from app.schemas.order import OrderResponse, OrderUpdateStatus
# from app.dependencies.auth import user_only,admin_only,get_current_user
# from app.utils.email_utils import send_email 
# from app.models.user import User
# from fastapi.security import HTTPBearer

# router = APIRouter(
#     prefix="/orders", 
#     tags=["Orders"], 
#     dependencies=[Depends(HTTPBearer())]
# )

# # 1. POST /api/orders - Place order (User)
# @router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
# def place_order(
#     db: Session = Depends(get_db), 
#     current_user = Depends(user_only)
# ):
#     cart_items = db.query(Cart).filter(Cart.user_id == current_user["user_id"]).all()
    
#     if not cart_items:
#         raise HTTPException(status_code=400, detail="Cart is empty")

#     total_price = 0
#     for item in cart_items:
#         food = db.query(Food).filter(Food.id == item.food_id).first()
#         if food:
#             total_price += food.price * item.quantity

#     new_order = Order(
#         user_id=current_user["user_id"],
#         total_price=total_price,
#         status="pending"
#     )
    
#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)
#     return new_order

# # 2. GET /api/orders - View orders (Filtered by role)
# @router.get("/", response_model=List[OrderResponse])
# def get_orders(
#     db: Session = Depends(get_db), 
#     current_user = Depends(get_current_user)
# ):
#     # If admin, show all orders; otherwise, show only the user's orders
#     if current_user.get("role") == "admin":
#         return db.query(Order).all()
    
#     return db.query(Order).filter(Order.user_id == current_user["user_id"]).all()

# # 3. PUT /api/orders/{id} - Admin Approval & Cart Clearance
# @router.put("/{order_id}", response_model=OrderResponse)
# def update_order_status(
#     order_id: int, 
#     data: OrderUpdateStatus, 
#     db: Session = Depends(get_db), 
#     current_user = Depends(admin_only)
# ):
#     if current_user.get("role") != "admin":
#         raise HTTPException(status_code=403, detail="Only admins can update order status")

#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     order.status = data.status

#     if data.status == "approved":
#         db.query(Cart).filter(Cart.user_id == order.user_id).delete()
    
#     db.commit()
#     db.refresh(order)
#     return order

# @router.put("/{order_id}", response_model=OrderResponse)
# def update_order_status(
#     order_id: int, 
#     data: OrderUpdateStatus, 
#     db: Session = Depends(get_db), 
#     current_user = Depends(admin_only)
# ):
#     order = db.query(Order).filter(Order.id == order_id).first()
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")

#     # 1. Update the status
#     order.status = data.status

#     # 2. Logic for Approval
#     if data.status == "approved":
#         # Clear the cart as we did before
#         db.query(Cart).filter(Cart.user_id == order.user_id).delete()
        
#         # 3. FETCH THE USER to get their email
#         # Assuming you have a relationship in your Order model, or query the User table
#         user = db.query(User).filter(User.id == order.user_id).first()
        
#         if user:
#             # 4. SEND THE NOTIFICATION EMAIL
#             send_email(
#                 to_email=user.email,
#                 subject="Your QuickBite Order is Approved!",
#                 context={
#                     "title": "Order Approved!",
#                     "name": user.name,
#                     "message": f"Great news! Your order #{order.id} has been approved and is now being prepared in the kitchen. Get ready for some deliciousness!",
#                     "action_url": "http://localhost:5173/order-history",
#                     "action_text": "Track Order"
#                 }
#             )
    
#     db.commit()
#     db.refresh(order)
#     return order


#UPDATED ORDER.PY:
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.order import Order
from app.models.cart import Cart
from app.models.food import Food
from app.models.user import User
from app.schemas.order import OrderResponse, OrderUpdateStatus
from app.dependencies.auth import user_only, admin_only, get_current_user
from app.utils.email_utils import send_email 
from fastapi.security import HTTPBearer

router = APIRouter(
    prefix="/orders", 
    tags=["Orders"], 
    dependencies=[Depends(HTTPBearer())]
)

# 1. POST /api/orders - Place order (User)
@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def place_order(
    db: Session = Depends(get_db), 
    current_user = Depends(user_only)
):
     # 1. NEWBUG FIX: Check if the user already has a pending order
    existing_order = db.query(Order).filter(
        Order.user_id == current_user["user_id"],
        Order.status == "pending"
    ).first()

    if existing_order:
        raise HTTPException(
            status_code=400, 
            detail="You already have an order pending approval. Please wait until it is processed."
        )
    cart_items = db.query(Cart).filter(Cart.user_id == current_user["user_id"]).all()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0
    for item in cart_items:
        food = db.query(Food).filter(Food.id == item.food_id).first()
        if food:
            total_price += food.price * item.quantity

    new_order = Order(
        user_id=current_user["user_id"],
        total_price=total_price,
        status="pending"
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# 2. GET /api/orders - View orders
@router.get("", response_model=List[OrderResponse])
def get_orders(
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    if current_user.get("role") == "admin":
        return db.query(Order).all()
    
    return db.query(Order).filter(Order.user_id == current_user["user_id"]).all()

# 3. PUT /api/orders/{order_id} - Admin Approval & Email Notification
@router.put("/{order_id}", response_model=OrderResponse)
def update_order_status(
    order_id: int, 
    data: OrderUpdateStatus, 
    background_tasks: BackgroundTasks, # Added for faster response
    db: Session = Depends(get_db), 
    current_user = Depends(admin_only)
):
    # Find the order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update the status
    order.status = data.status

    # If approved, clear cart and send email
    if data.status == "approved":
        # Clear the customer's cart
        db.query(Cart).filter(Cart.user_id == order.user_id).delete()
        
        # Get user details for the email
        user = db.query(User).filter(User.id == order.user_id).first()
        
        if user:
            # Send email in the background so the API returns instantly
            background_tasks.add_task(
                send_email,
                to_email=user.email,
                subject="Your QuickBite Order is Approved!",
                context={
                    "title": "Order Approved!",
                    "name": user.name,
                    "message": f"Great news! Your order #{order.id} has been approved and is now being prepared in the kitchen. Get ready for some deliciousness!",
                    "action_url": "http://localhost:5173/order-history",
                    "action_text": "Track My Order"
                }
            )
    
    db.commit()
    db.refresh(order)
    return order
