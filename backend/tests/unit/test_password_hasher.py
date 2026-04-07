from src.app.adapters.outbound.security.password_hasher import PasswordHasher


def test_hash_and_verify_success() -> None:
    hasher = PasswordHasher()
    hashed = hasher.hash("Secret123!")

    assert hashed != "Secret123!"
    assert hasher.verify("Secret123!", hashed) is True


def test_verify_fails_with_wrong_password() -> None:
    hasher = PasswordHasher()
    hashed = hasher.hash("Secret123!")
    assert hasher.verify("Wrong123!", hashed) is False