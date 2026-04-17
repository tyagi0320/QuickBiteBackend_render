# from app.repositories.user_repo import get_user_by_email , create_user, email_exists
# from app.models.user import User
# from app.core.security import(
#     verify_password, 
#     create_access_token, 
#     create_refresh_token, hash_password)
# from app.utils.email_utils import send_email
# from fastapi import HTTPException
# import random
# from datetime import datetime, timedelta,timezone
# from fastapi import HTTPException, status


# def generate_otp():
#     return str(random.randint(100000, 999999))


# def otp_expiry():
#     return datetime.now(timezone.utc) + timedelta(minutes=10)


# def register_user(db, data):
#     if email_exists(db, data.email):
#         raise HTTPException(status_code=409, detail="Email already registered")

#     hashed_pwd = hash_password(data.password)
#     user_dict = data.dict()
#     user_dict.pop("password")  
    
#     user = User(
#         **user_dict, 
#         hashed_password=hashed_pwd
#     )

#     user.otp = generate_otp()
#     user.otp_expires_at = otp_expiry()

#     db.add(user)
#     db.commit()
#     db.refresh(user)

#     # send_email(
#     #     to_email=user.email,
#     #     subject="Your verification code",
#     #     context={
#     #         "title": "Verify your email",
#     #         "name": user.email,
#     #         "message": f"Your OTP is {user.otp}. It expires in 10 minutes.",
#     #         "action_url": "",
#     #         "action_text": ""
#     #     }
#     # )

#     return {"message": "User Registered Successfully"}

# def login_user(db, data):
#     user = get_user_by_email(db, data.email)

#     if not user:
#         return None

#     if not verify_password(data.password, user.hashed_password):
#         return None

#     access_token = create_access_token({"user_id": user.id, "role": user.role})
#     refresh_token = create_refresh_token({"user_id": user.id, "role": user.role})

#     return access_token, refresh_token, user


# def resend_otp(db, email: str):
#     user = get_user_by_email(db, email)

#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )

#     if user.is_verified:
#         raise HTTPException(
#             status_code=400,
#             detail="Email already verified"
#         )

#     # Anti-spam cooldown (60 seconds)
#     if user.otp_sent_at:
#         if datetime.now(timezone.utc) - user.otp_sent_at < timedelta(seconds=60):
#             raise HTTPException(
#                 status_code=429,
#                 detail="Please wait before requesting another OTP"
#             )

#     user.otp = generate_otp()
#     user.otp_expires_at = otp_expiry()
#     user.otp_sent_at = datetime.now(timezone.utc)

#     db.commit()

#     send_email(
#         to_email=user.email,
#         subject="Your new OTP",
#         context={
#             "title": "OTP Verification",
#             "name": user.email,
#             "message": f"Your new OTP is {user.otp}. It expires in 10 minutes.",
#             "action_url": "",
#             "action_text": ""
#         }
#     )

#     return {"message": "OTP resent successfully"}


##########FOLLOWING CODE IS FOR EMAIL-BASED AUTH#######################



from app.repositories.user_repo import get_user_by_email , create_user, email_exists
from app.models.user import User
from app.core.security import(
    verify_password, 
    create_access_token, 
    create_refresh_token, hash_password)
from app.utils.email_utils import send_email
from fastapi import HTTPException
import random
from datetime import datetime, timedelta,timezone
from fastapi import HTTPException, status


def generate_otp():
    return str(random.randint(100000, 999999))


def otp_expiry():
    return datetime.now(timezone.utc) + timedelta(minutes=10)


def register_user(db, data):
    if email_exists(db, data.email):
        raise HTTPException(status_code=409, detail="Email already registered")

    hashed_pwd = hash_password(data.password)
    user_dict = data.dict()
    user_dict.pop("password")  
    
    user = User(
        **user_dict, 
        hashed_password=hashed_pwd
    )

    user.otp = generate_otp()
    user.otp_expires_at = otp_expiry()

    db.add(user)
    db.commit()
    db.refresh(user)

    send_email(
        to_email=user.email,
        subject="Verify your QuickBite Account",
        context={
            "title": "Welcome to QuickBite!",
            "name": user.name,
            "message": f"Your verification code is {user.otp}. This code expires in 10 minutes.",
        }
    )

    return {"message": "OTP sent to email. Please verify to login."}


def login_user(db, data):
    user = get_user_by_email(db, data.email)

    if not user or not verify_password(data.password, user.hashed_password):
        return None

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Account not verified. Please verify your email via OTP."
        )

    access_token = create_access_token({"user_id": user.id, "role": user.role})
    refresh_token = create_refresh_token({"user_id": user.id, "role": user.role})

    return access_token, refresh_token, user


def resend_otp(db, email: str):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email already verified"
        )

    # Anti-spam cooldown (60 seconds)
    if user.otp_sent_at:
        if datetime.now(timezone.utc) - user.otp_sent_at < timedelta(seconds=60):
            raise HTTPException(
                status_code=429,
                detail="Please wait before requesting another OTP"
            )

    user.otp = generate_otp()
    user.otp_expires_at = otp_expiry()
    user.otp_sent_at = datetime.now(timezone.utc)

    db.commit()

    send_email(
        to_email=user.email,
        subject="Your new OTP",
        context={
            "title": "Welcome to QuickBite!",
            "name": user.name,
            "message": f"Your verification code is {user.otp}. This code expires in 10 minutes.",
            "action_url": "#",      # Add these to prevent template errors
            "action_text": "Verify Now" 
        }
    )

    return {"message": "OTP resent successfully"}

