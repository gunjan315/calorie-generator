from fastapi import APIRouter, Depends
from models.schema import CreateUserSchema
from models.schema import UserLoginSchema, UserResponseSchema, TokenSchema
from controllers.auth_controller import AuthController, get_auth_controller
router = APIRouter()

@router.post("/register", response_model=UserResponseSchema)
async def register(
    user_data: CreateUserSchema,
    auth_controller: AuthController = Depends(get_auth_controller)
) -> UserResponseSchema:
    return await auth_controller.register(user_data)


@router.post("/login", response_model=TokenSchema)
async def login(
    credentials: UserLoginSchema,
    auth_controller: AuthController = Depends(get_auth_controller)
) -> TokenSchema:
    return await auth_controller.login(credentials)