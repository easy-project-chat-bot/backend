from fastapi import Request
from sqlalchemy.orm import Session
from models import db_session, User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(username: str, password: str) -> bool:
    user = db_session.query(User).filter(User.username == username).first()
    if user:
        return False
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db_session.add(new_user)
    db_session.commit()
    return True

def authenticate_user(username: str, password: str):
    user = db_session.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def get_current_user(request: Request):
    user_id = request.session.get("user")
    if not user_id:
        return None
    return db_session.query(User).filter(User.id == user_id).first()