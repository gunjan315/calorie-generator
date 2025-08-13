import logging
from models.schema import (CalorieRequestSchema, CalorieResponseSchema)
from services.usda_service import USDAService


class CalorieCalculatorService:
    def __init__(
        self, 
        usda_service: USDAService
    ):
        self.usda_service = usda_service

    async def calculate_calories(self, request: CalorieRequestSchema) -> CalorieResponseSchema:
        try:
            food_data = await self.usda_service.search_food(request.dish_name)
            if not food_data:
                raise Exception(f"Dish '{request.dish_name}' not found..")

            calories_per_100g = food_data['calories-per-100g']
            total_calories = calories_per_100g * request.servings
            corrected_dish_name = food_data.get('description', request.dish_name)
            
            response_data = request.model_dump()
            response_data['dish_name'] = corrected_dish_name

            return CalorieResponseSchema(
                **response_data,
                calories_per_serving=round(calories_per_100g, 2),
                total_calories=round(total_calories, 2),
            )
        except Exception as ex:
            logging.error(f"Error calculating calories:{ex}")
            raise Exception(f"Error fetching calories:{str(ex)}")