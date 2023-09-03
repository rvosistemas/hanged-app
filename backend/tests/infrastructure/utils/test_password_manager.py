from ....application.infrastructure.utils.passwordManager import PasswordManager


def test_encrypt_password():
    password = "test_password"
    hashed_password = PasswordManager.encrypt_password(password)
    assert hashed_password is not None
    assert len(hashed_password) > 0


def test_verify_password():
    password = "test_password"
    hashed_password = PasswordManager.encrypt_password(password)
    assert PasswordManager.verify_password(password, hashed_password) is True

    wrong_password = "wrong_password"
    assert PasswordManager.verify_password(wrong_password, hashed_password) is False
