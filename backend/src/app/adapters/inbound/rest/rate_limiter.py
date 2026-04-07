from slowapi import Limiter
from slowapi.util import get_remote_address

from src.app.bootstrap.settings import settings

limiter = Limiter(key_func=get_remote_address)
LOGIN_RATE_LIMIT = settings.AUTH_RATE_LIMIT_LOGIN
