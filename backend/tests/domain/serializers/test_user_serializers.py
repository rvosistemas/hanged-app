from ....application.domain.serializers.userSerializers import (
    UserSerializer,
)


class FakeUser:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


def test_user_serializer():
    fake_user = FakeUser("test_user", "password123", "user")

    serializer = UserSerializer(fake_user)

    expected_data = {"username": "test_user", "password": "password123", "role": "user"}
    assert serializer.to_dict() == expected_data
