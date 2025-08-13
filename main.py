import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from config import settings
from database.connection import database
from routes.api import api_router    
from middleware.rate_limiter import rate_limit_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await database.connect()
        logging.info("Application started..")
        yield
    finally:
        # closing conn
        await database.close_conn()
        logging.info("Application shut successfuly..")

def create_app() -> FastAPI:
    logging.info("Initialising fastAPI")

    is_prod = "prod" in settings.environment.lower()
    docs_url = None if is_prod else "/docs"
    redoc_url = None if is_prod else "/redoc"

    app = FastAPI(title="Calorie Counter", docs_url=docs_url, redoc_url=redoc_url, lifespan=lifespan)

    @api_router.get("/")
    async def healthcheck() -> dict:
        return {
            "service": "Calorie Counter",
            "version": "v1",
            # "release_commit": settings.release_commit_short,
        }
    
    # Enhanced CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add rate limiting middleware
    app.middleware("http")(rate_limit_middleware)


    @app.get("/")
    async def healthcheck() -> dict:
        return {
            "service": "Calorie counter",
            "version": "v1",
        }

    app.include_router(api_router)
    return app

try:
    app = create_app()
except Exception as e:
    logging.error(f"Error:{e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888, log_level="info")
