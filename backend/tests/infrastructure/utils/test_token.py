import pytest
from jose import jwt
from datetime import timedelta
from ....application.infrastructure.utils.token import create_access_token, verify_token
from ....application.infrastructure.core.settings import Settings


def test_create_access_token():
    username = "test_user"
    expires_delta = timedelta(minutes=30)

    access_token = create_access_token(username, expires_delta)
    assert access_token is not None
    assert isinstance(access_token, str)

    settings = Settings()
    decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    assert decoded_token["sub"] == username

    access_token = create_access_token(username)
    assert access_token is not None


def test_verify_token():
    username = "test_user"
    expires_delta = timedelta(minutes=30)

    access_token = create_access_token(username, expires_delta)
    verified_username = verify_token(access_token)
    assert verified_username == username

    with pytest.raises(Exception):
        verify_token("wrong_token")
