from models import db_session, User
from fastapi import Request

# Поиск по логину
def get_user_by_username(username: str):
    return db_session.query(User).filter(User.username == username).first()

# Регистрация
def register_user(name, surname, username, email, password):
    if get_user_by_username(username):
        return None
    user = User(name=name, surname=surname, username=username, email=email, password=password)
    db_session.add(user)
    db_session.commit()
    return user

# Авторизация
def authenticate_user(username, password):
    user = get_user_by_username(username)
    if user and user.password == password:
        return user
    return None

# Получить текущего пользователя из сессии
def get_current_user(request: Request):
    user_id = request.session.get("user_id")
    if user_id:
        return db_session.query(User).filter(User.id == user_id).first()
    return None