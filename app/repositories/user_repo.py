from app.models.user import User

def get_user_by_email(db, email):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db, user):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def email_exists(db , email: str) -> bool:
    return db.query(User).filter(User.email == email).first() is not None