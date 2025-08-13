from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.schema import UserResponseSchema
from services.factory import get_auth_service

security = HTTPBearer()
auth_service = get_auth_service()


async def get_curr_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> UserResponseSchema:
    try:
        res = await auth_service.get_current_user(credentials.credentials)
        if res is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid auth credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return res
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )