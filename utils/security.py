from passlib.context import CryptContext
from config import get_settings

from jose import jwt
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"])
settings = get_settings()


class SecurityUtils:
    @staticmethod
    def verify_password(plain_pwd: str, hashed_pwd: str):
        return pwd_context.verify(plain_pwd, hashed_pwd)

    @staticmethod
    def get_pwd_hash(pwd: str) -> str:
        return pwd_context.hash(pwd)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expiry_time)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.jwt_key, algorithm=settings.jwt_algo)
        


    @staticmethod
    def verify_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.jwt_key, algorithms=[settings.jwt_algo])
        except Exception as ex:
            return None