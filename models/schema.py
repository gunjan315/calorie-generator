from datetime import datetime
from typing import Optional
from typing import List
from pydantic import BaseModel, Field, EmailStr, field_validator


class CalorieRequestSchema(BaseModel):
    dish_name: str = Field(...,min_length=1,max_length=200)
    servings: float = Field(...,le=100,gt=0)
    
    # Basic validations
    @field_validator('servings')
    def validate_servings(cls, v:float):
        if v <= 0:
            raise ValueError('Servings should be greater than 0!')
        if v > 100:
            raise ValueError('Servings cannot be more than 100!')
        # return round(v, 2)
        return v
    
    @field_validator('dish_name')
    def validate_dish(cls, v: str) -> str:
        val = v.strip()
        if not val:
            raise ValueError('Dish name cannot be empty, please enter valid dish name!')
        if any(char.isdigit() for char in val) and len(val) < 3:
            raise ValueError('Invalid dish name format found!')
        return val


class CalorieResponseSchema(BaseModel):
    dish_name: str
    servings: float
    calories_per_serving: float
    total_calories: float
    source: str = "USDA Food Database"


class CreateUserSchema(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50)
    
    # General pwd validation... might be used in API
    @field_validator('password')
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError('Password should be at least 8 characters long!')
        if not any(c.isupper() for c in v):
            raise ValueError('Password should contain at least one uppercase letter!')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter!')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password should contain at least one digit!')
        return v


class UserResponseSchema(BaseModel):
    # using alias for mongo
    id: Optional[str] = Field(None, alias="_id")
    first_name: str
    last_name: str
    email: str
    created_at: datetime
    
    # class Config:
    #     populate_by_name = True



class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str



class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int

class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


