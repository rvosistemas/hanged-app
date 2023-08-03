from sqlalchemy import Column, String

from .Entity import Entity
from .Enums import StatusEnum, RoleEnum


class User(Entity):
    __tablename__ = "users"

    username = Column(String(50), nullable=False, index=True, unique=True)
    password = Column(String(50), nullable=False, index=True)
    role = Column(String(50), nullable=False, index=True, default=RoleEnum.FINAL_USER.value)
    status = Column(String(50), nullable=False, index=True, default=StatusEnum.ACTIVE.value)
