from datetime import datetime
from typing import List
from sqlalchemy.orm import Session

from ..models.User import User
from ..models.Enums import RoleEnum, StatusEnum


class UserSqlRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_users(self, filters: dict = None) -> List[User]:
        filters = filters or {}
        return self.db.query(User).all()

    def get_user_by_id(self, id: int) -> User:
        return self.db.query(User).filter(User.id == id).first()

    def get_user_by_username(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()

    def get_user_count(self) -> int:
        return self.db.query(User).count()

    def create_user(self, user_data: dict) -> User:
        user = User(
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            created_by=user_data["username"],
            updated_by=user_data["username"],
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User, user_data: dict) -> None:
        user.username = user_data["username"]
        user.password = user_data["password"]
        user.role = user_data["role"]
        user.status = user_data["status"]
        user.updated_at = datetime.now()
        user.updated_by = user_data["username"]
        self.db.commit()
        self.db.refresh(user)

    def remove_user(self, user: User) -> None:
        user.status = "inactive"
        user.updated_at = datetime.now()
        user.updated_by = user.username
        self.db.commit()
        self.db.refresh(user)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        self.db.delete(user)
        self.db.commit()
