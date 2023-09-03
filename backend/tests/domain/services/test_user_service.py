from ....application.domain.services.UserService import UserService
from ....application.domain.models.User import User
from unittest.mock import Mock

mock_repository = Mock()
user_service = UserService(repository=mock_repository)


def test_get_all_users():
    mock_repository.get_all_users.return_value = [User(id=1, username="user1")]
    users = user_service.get_all_users()

    # Verify that the method was called in the repository and that the expected result was returned
    mock_repository.get_all_users.assert_called_once_with(None)
    assert len(users) == 1
    assert users[0].username == "user1"


def test_get_user_by_id():
    mock_repository.get_user_by_id.return_value = User(id=1, username="user1")
    user = user_service.get_user_by_id(1)

    mock_repository.get_user_by_id.assert_called_once_with(1)
    assert user.username == "user1"


def test_get_user_by_username():
    mock_repository.get_user_by_username.return_value = User(id=1, username="user1")
    user = user_service.get_user_by_username("user1")

    mock_repository.get_user_by_username.assert_called_once_with("user1")
    assert user.username == "user1"


def test_get_user_count():
    mock_repository.get_user_count.return_value = 1
    count = user_service.get_user_count()

    mock_repository.get_user_count.assert_called_once_with()
    assert count == 1


def test_create_user():
    user_data = {
        "username": "test_user",
        "password": "password123",
        "role": "admin",
        "status": "active",
    }
    mock_repository.create_user.return_value = User(id=1, username="test_user")
    user = user_service.create_user(user_data)

    mock_repository.create_user.assert_called_once_with(user_data)
    assert user.username == "test_user"


def test_update_user():
    user_data = {
        "username": "test_user",
        "password": "password123",
        "role": "admin",
        "status": "active",
    }
    user = User(id=1, username="test_user")
    mock_repository.update_user.return_value = None
    user_service.update_user(user, user_data)

    mock_repository.update_user.assert_called_once_with(user, user_data)


def test_remove_user():
    user = User(id=1, username="test_user")
    mock_repository.remove_user.return_value = None
    user_service.remove_user(user)

    mock_repository.remove_user.assert_called_once_with(user)


def test_delete_user():
    user = User(id=1, username="test_user")
    mock_repository.delete_user.return_value = None
    user_service.delete_user(user)

    mock_repository.delete_user.assert_called_once_with(user)
