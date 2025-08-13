from fastapi import HTTPException, Depends
from models.schema import CreateUserSchema, UserLoginSchema, UserResponseSchema, TokenSchema
from services.factory import get_auth_service
from services.auth_service import AuthenticationService
import logging


class AuthController:
    def __init__(self, auth_service: AuthenticationService):
        self.auth_service = auth_service


    async def login(self, credentials: UserLoginSchema) -> TokenSchema:
        try:
            user = await self.auth_service.authenticate_user(credentials)
            if not user:
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect email or password.."
                )
            
            return self.auth_service.create_token(user)
        except Exception as e:
            logging.error(f"Error logging in:{e}")
            raise HTTPException(status_code=500, detail="Login failed")


    async def register(self, user_data: CreateUserSchema) -> UserResponseSchema:
        try:
            return await self.auth_service.register_user(user_data)
        except Exception as e:
            logging.error(f"Registration error: {e}")
            if "Email already registered" in str(e):
                raise HTTPException(status_code=400, detail="Email already registered")
            raise HTTPException(status_code=500, detail="Registration failed")


def get_auth_controller(auth_service: AuthenticationService = Depends(get_auth_service)) -> AuthController:
    return AuthController(auth_service)