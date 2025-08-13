from fastapi import APIRouter, Depends
from models.schema import CalorieRequestSchema, CalorieResponseSchema, UserResponseSchema
from controllers.calorie_controller import get_calorie_controller, CalorieController
from middleware.auth_middleware import get_curr_user

router = APIRouter()


@router.post("/get-calories", response_model=CalorieResponseSchema)
async def get_calories(
    request: CalorieRequestSchema,
    _ : UserResponseSchema = Depends(get_curr_user),
    calorie_controller: CalorieController = Depends(get_calorie_controller)
):
    return await calorie_controller.get_calories(request)