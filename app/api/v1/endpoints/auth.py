from fastapi import APIRouter, Depends, HTTPException, Request, Response
from app.core.database import get_db
from app.schemas.user import UserRegister, UserLogin
from app.core.security import(
    decode_refresh_token,
    create_access_token,
)
from app.repositories.user_repo import get_user_by_email
from datetime import datetime, timezone
from fastapi import Query
from app.repositories.user_repo import get_user_by_id
from sqlalchemy.orm import Session
from app.services.auth_service import register_user, login_user, resend_otp
from app.utils.email_utils import send_email


router = APIRouter(tags=["Auth"])


@router.post("/register")
def register(data: UserRegister, db = Depends(get_db)):
    return register_user(db, data)


@router.post("/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(404, "User not found")

    if user.is_verified:
        return {"message": "Account already verified"}

    # Check if OTP matches and is not expired
    if user.otp != otp:
        raise HTTPException(400, "Invalid OTP")

    if datetime.now(timezone.utc) > user.otp_expires_at:
        raise HTTPException(400, "OTP has expired")

    user.is_verified = True
    user.otp = None # Clear OTP after success
    user.otp_expires_at = None
    db.commit()

    return {"message": "Email verified successfully. You can now login."}


@router.post("/resend-otp")
def resend_otp_api(email: str, db=Depends(get_db)):
    return resend_otp(db, email)


@router.post("/login")
def login(
    request: Request,
    data: UserLogin,
    response: Response,
    db=Depends(get_db)
):
    result = login_user(db, data)
    if not result:
        raise HTTPException(401, "Invalid credentials")

    access_token, refresh_token, user = result

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,          
        samesite="lax",        
        max_age=7 * 24 * 60 * 60,
    )

    return {
        "access_token": access_token,
        "message": "Login Successfull",
    }


@router.post("/refresh")
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(401, "Refresh token missing")

    payload = decode_refresh_token(refresh_token)

    new_access_token = create_access_token(
        {"user_id": payload["user_id"],
         "role": payload["role"]}
          
    )

    return {
        "access_token": new_access_token
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}

