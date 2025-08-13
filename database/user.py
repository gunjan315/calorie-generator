from datetime import datetime, timezone
from typing import Optional

import logging

from bson import ObjectId

from .connection import database

class UserRepo:
    def __init__(self):
        self.collection_name = "users"
        self._collection = None

    @property
    def collection(self):
        if self._collection is None:
            self._collection = database.get_mongo_collection(self.collection_name)
        return self._collection

    async def create_user(self, payload: dict) -> dict:
        try:
            payload['created_at'] = datetime.now(timezone.utc)
            result = await self.collection.insert_one(payload)
            payload['_id'] = result.inserted_id
            return payload
        except Exception as ex:
            logging.error(f"Error while creating user: {ex}")
            raise ex

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        try:
            return await self.collection.find_one({"email": email})
        except Exception as e:
            logging.error(f"Error finding user by email id: {e}")
            return None

    async def does_email_exist(self, email: str):
        try:
            result = await self.collection.find_one({"email": email})
            return result is not None
        except Exception as e:
            logging.error(f"Error checking if email exists: {e}")
            return False

    async def find_by_id(self, id: str) -> Optional[dict]:
        try:
            return await self.collection.find_one({"_id": ObjectId(id)})
        except Exception as ex:
            logging.error(f"Error finding user by id: {ex}")
            return None

    