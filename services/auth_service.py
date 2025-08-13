from typing import Optional
from models.schema import (CreateUserSchema, UserLoginSchema, UserResponseSchema, TokenSchema)

from database.user import UserRepo
from utils.security import SecurityUtils

import logging


class AuthenticationService:
    def __init__(self, user_repo: UserRepo, security_utils: SecurityUtils):
        self.user_repository = user_repo
        self.security_utils = security_utils


    async def register_user(self, user_data: CreateUserSchema) -> UserResponseSchema:
        try:
            if await self.user_repository.does_email_exist(user_data.email):
                raise Exception("Email already registered!")

            # storing hash pwd for security reasons.. we should generally just match the hash
            # pwd for authentication
            hashed_password = self.security_utils.get_pwd_hash(user_data.password)
            
            user_payload = {
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "email": user_data.email,
                "hashed_password": hashed_password
            }

            res = await self.user_repository.create_user(user_payload)
            user_dict = {key: value for key, value in res.items() if key != "_id"}
            user_dict["id"] = str(res["_id"])

            return UserResponseSchema(
                **user_dict,
            )

        except Exception as ex:
            logging.error(f"Error creating user: {ex}")
            raise ex

    async def authenticate_user(self, creds: UserLoginSchema) -> Optional[UserResponseSchema]:
        try:
            user = await self.user_repository.get_user_by_email(creds.email)
            if not user or not self.security_utils.verify_password(creds.password, user["hashed_password"]):
                return None
            user_dict = {key: value for key, value in user.items() if key != "_id"}
            user_dict["id"] = str(user["_id"])
            
            return UserResponseSchema(**user_dict)


        except Exception as e:
            logging.error(f"User Authetnication failed:{e}")
            return None

    def create_token(self, user_payload: UserResponseSchema) -> TokenSchema:
        token_info = {"email": user_payload.email, "user_id": str(user_payload.id)}
        access_token = self.security_utils.create_access_token(token_info)
        return TokenSchema(access_token=access_token)

    async def get_current_user(self, token: str) -> Optional[UserResponseSchema]:
        try:
            payload = self.security_utils.verify_token(token)
            if payload is None:
                return None

            if payload.get("email") is None:
                return None

            user = await self.user_repository.get_user_by_email(payload.get("email"))
            if user is None:
                return None

            user_dict = {k: v for k, v in user.items() if k != "_id"}
            user_dict["id"] = str(user["_id"])
            
            return UserResponseSchema(**user_dict)


        except Exception as ex:
            logging.error(f"Error fetching user: {ex}")
            return None