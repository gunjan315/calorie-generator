#NOTE: Could be used later


# from fastapi import HTTPException, status


# class CalorieCalcException(HTTPException):
#     def __init__(self, detail: str):
#         super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


# class FoodNotFoundException(HTTPException):
#     def __init__(self, dish_name: str):
#         detail = f"Food '{dish_name}' not present in USDA database... Try different spelling or more generic term"
#         super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


# class USDAapiException(HTTPException):
#     def __init__(self, detail: str):
#         super().__init__(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"USDA API error:{detail}")