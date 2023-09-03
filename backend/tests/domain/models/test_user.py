from ....application.domain.models.User import User, StatusEnum, RoleEnum


def test_user_creation():
    user = User(
        username="test_user", password="password123", role=RoleEnum.ADMIN.value, status=StatusEnum.INACTIVE.value
    )

    assert user.username == "test_user"
    assert user.password == "password123"
    assert user.role == RoleEnum.ADMIN.value
    assert user.status == StatusEnum.INACTIVE.value
