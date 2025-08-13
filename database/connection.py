from config import get_settings
from motor.motor_asyncio import AsyncIOMotorClient
import logging


class DatabaseInstantiation:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.database = None

    async def connect(self):
        settings = get_settings()
        self.client = AsyncIOMotorClient(settings.mongo_url)
        self.database = self.client[settings.mongodb_database_name]

        try:
            await self.client.admin.command('ping')
            logging.info("Mongo connection successful!")
        except Exception as e:
            logging.error(f"Mongo connection failed due to: {e}")
            raise e

    async def close_conn(self):
        if self.client:
            self.client.close()
            logging.info("Mongo connection closed successfully!")

    def get_mongo_collection(self, name: str):
        return self.database[name]


database = DatabaseInstantiation()