from passlib.context import CryptContext

pwd = CryptContext(schemes=["argon2"], deprecated="auto")


class PasswordHasher:
    def hash(self, raw_password: str) -> str:
        return pwd.hash(raw_password)

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        return pwd.verify(raw_password, hashed_password)