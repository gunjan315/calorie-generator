from fastapi import HTTPException, Depends
from services.factory import get_calorie_service
from models.schema import CalorieRequestSchema, CalorieResponseSchema
import logging

from services.calorie_service import CalorieCalculatorService

class CalorieController:    
    def __init__(self, calorie_service: CalorieCalculatorService):
        self.calorie_service = calorie_service

    async def get_calories(self, request: CalorieRequestSchema) -> CalorieResponseSchema:
        try:
            return await self.calorie_service.calculate_calories(request)
        except Exception as e:
            logging.error(f"Error calculating calories:{e}")
            if "not found" in str(e).lower():
                raise HTTPException(
                    status_code=404,
                    detail=f"Dish '{request.dish_name}' not found"
                )
            raise e


def get_calorie_controller(calorie_service: CalorieCalculatorService = Depends(get_calorie_service)) -> CalorieController:
    return CalorieController(calorie_service)