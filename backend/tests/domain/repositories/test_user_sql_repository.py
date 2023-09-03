from datetime import datetime

from ....application.domain.repositories.UserSqlRepository import UserSqlRepository
from ....application.domain.models.Enums import StatusEnum, RoleEnum


# db_session is a fixture from conftest.py
def test_user_sql_repository(db_session):
    repo = UserSqlRepository(db_session)

    user_data = {
        "username": "test_user",
        "password": "password123",
        "role": RoleEnum.ADMIN.value,
        "status": StatusEnum.ACTIVE.value,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "created_by": "test_user",
        "updated_by": "test_user",
    }

    created_user = repo.create_user(user_data)
    retrieved_user = repo.get_user_by_username("test_user")
    assert created_user == retrieved_user

    updated_data = {
        "username": "updated_user",
        "password": "updated_password",
        "role": "admin",
        "status": "inactive",
    }
    repo.update_user(created_user, updated_data)
    updated_user = repo.get_user_by_id(created_user.id)
    assert updated_user.username == "updated_user"
    assert updated_user.password == "updated_password"
    assert updated_user.role == "admin"
    assert updated_user.status == "inactive"

    users = repo.get_all_users()
    assert len(users) == 1

    # users = repo.get_all_users({"status": "inactive"})

    count = repo.get_user_count()
    assert count == 1

    repo.remove_user(updated_user)
    removed_user = repo.get_user_by_id(updated_user.id)
    assert removed_user.status == "inactive"

    repo.delete_user(updated_user.id)
    deleted_user = repo.get_user_by_id(updated_user.id)
    assert deleted_user is None
