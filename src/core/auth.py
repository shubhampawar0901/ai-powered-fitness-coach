from sqlalchemy.orm import Session
from .database import User

class AuthService:
    def __init__(self):
        pass

    def authenticate_user(self, db: Session, username: str, password: str) -> User:
        user = db.query(User).filter(User.username == username).first()
        if user and user.password == password:
            return user
        return None

    def create_user(self, db: Session, username: str, password: str) -> User:
        user = User(username=username, password=password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def generate_token(self, user: User) -> str:
        return f"token_{user.id}_{user.username}"
