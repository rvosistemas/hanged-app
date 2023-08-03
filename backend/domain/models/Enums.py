from enum import Enum


class RoleEnum(str, Enum):
    FINAL_USER = "final_user"
    ADMIN = "admin"
    OWNER = "owner"
    GUEST = "guest"
    MODERATOR = "moderator"


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
