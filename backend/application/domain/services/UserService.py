from typing import List

from ..repositories.UserSqlRepository import UserSqlRepository
from ..models.User import User


class UserService:
    def __init__(self, repository: UserSqlRepository):
        self.repository = repository

    def get_all_users(self, filters: dict = None) -> List[User]:
        users = self.repository.get_all_users(filters)
        return users

    def get_user_by_id(self, user_id: str) -> User:
        user = self.repository.get_user_by_id(user_id)
        return user

    def get_user_by_username(self, user_username: str) -> User:
        user = self.repository.get_user_by_username(user_username)
        return user

    def get_user_count(self) -> int:
        users_count = self.repository.get_user_count()
        return users_count

    def create_user(self, user_data: dict) -> User:
        user = self.repository.create_user(user_data)
        return user

    def update_user(self, user: User, user_data: dict) -> None:
        self.repository.update_user(user, user_data)

    def remove_user(self, user: User) -> None:
        self.repository.remove_user(user)

    def delete_user(self, user: User) -> None:
        self.repository.delete_user(user)
