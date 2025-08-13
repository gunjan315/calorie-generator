"""
services factory for dependencyy injection
"""
from functools import lru_cache
from database.user import UserRepo
from services.auth_service import AuthenticationService
from services.fuzzy_matcher import FuzzyMatcherService
from services.usda_service import USDAService
from services.calorie_service import CalorieCalculatorService
from utils.security import SecurityUtils

# Added LRU cache to improve performance 

@lru_cache()
def get_user_repository() -> UserRepo:
    """Get user repo instance"""
    return UserRepo()


@lru_cache()
def get_security_utils() -> SecurityUtils:
    return SecurityUtils()


@lru_cache()
def get_fuzzy_matcher() -> FuzzyMatcherService:
    return FuzzyMatcherService()


@lru_cache()
def get_usda_service() -> USDAService:
    return USDAService(get_fuzzy_matcher())


@lru_cache()
def get_calorie_service() -> CalorieCalculatorService:
    """Get calorie calc service instance"""
    return CalorieCalculatorService(get_usda_service())


@lru_cache()
def get_auth_service() -> AuthenticationService:
    return AuthenticationService(get_user_repository(), get_security_utils())