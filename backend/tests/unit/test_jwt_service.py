from src.app.adapters.outbound.security.jwt_service import JwtService


def test_create_and_decode_token() -> None:
    svc = JwtService(secret="test-secret", algorithm="HS256", expire_minutes=30)
    token = svc.create_access_token(sub="1", email="a@b.com", roles=["user"])
    payload = svc.decode_token(token)

    assert payload["sub"] == "1"
    assert payload["email"] == "a@b.com"
    assert "user" in payload["roles"]


def test_create_and_decode_refresh_token() -> None:
    svc = JwtService(secret="test-secret", algorithm="HS256", expire_minutes=30)
    token = svc.create_refresh_token(sub="1", email="a@b.com", roles=["user"])
    payload = svc.decode_token(token)
    assert payload["type"] == "refresh"