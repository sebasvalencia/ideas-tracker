from typing import Protocol


class PasswordHasherPort(Protocol):
    def hash(self, raw_password: str) -> str:
        ...

    def verify(self, raw_password: str, hashed_password: str) -> bool:
        ...