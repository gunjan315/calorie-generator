import asyncio
import hashlib
from typing import List, Optional, Dict, Any
import httpx
from config import settings

from services.fuzzy_matcher import FuzzyMatcherService
from utils.cache import cache


import logging


class USDAService:
    def __init__(self, fuzzy_matcher: FuzzyMatcherService):
        self.fuzzy_matcher = fuzzy_matcher
        self.api_key = settings.api_key
        self.base_url = settings.base_url

    def _generate_cache_key(self, query: str) -> str:
        return f"usda_cache_{hashlib.md5(query.lower().encode()).hexdigest()}"

    async def _make_request(self, path: str, params: dict) -> dict:
        params['api_key'] = self.api_key
        url = f"{self.base_url}/{path}"
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=42) as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    return response.json()
            except httpx.HTTPError as ex:
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
                    continue
                logging.error(f"USDA API error after {max_retries} tries: {ex}")
                raise Exception(f"Failed to fetch from USDA api.")

    def _extract_calories(self, data: dict) -> Optional[float]:
        nutrients = data.get('foodNutrients', [])
        for nutrient in nutrients:
            if (nutrient.get('nutrientName', '').lower() == 'energy' and 
                    nutrient.get('unitName', '').upper() == 'KCAL' and 
                    nutrient.get('value') is not None):
                    return float(nutrient.get('value'))
            
        return

    async def search_food(self, query: str) -> Optional[dict]:
        cache_key = self._generate_cache_key(query)
        cached_result = await cache.get_value(cache_key)
        if cached_result:
            logging.info(f"Cache found for query: {query}")
            return cached_result

        try:
            params = {
                'query': query,  
                'pageSize': 25,
            }
            
            response = await self._make_request('foods/search', params)
            foods = response.get('foods', [])
            
            if not foods:
                logging.info(f"No foods found for query: {query}")
                return 

            descriptions = []
            
            valid_foods = []
            for food in foods:
                calories = self._extract_calories(food)
                if calories and calories > 0:
                    food_info = {
                        'description': food.get('description', ''),
                        'calories-per-100g': calories,
                        'fdc_id': food.get('fdcId')
                    }
                    valid_foods.append(food_info)
                    descriptions.append(food_info['description'])

            if not valid_foods:
                logging.info(f"No foods found with {query}")
                return None

            best_match_desc = self.fuzzy_matcher.find_best_match(query, descriptions)
            
            result = None
            if best_match_desc:
                for food in valid_foods:
                    if food['description'] == best_match_desc:
                        result = food
                        break
                logging.info(f"Fuzzy match found!: {best_match_desc}")
            else:
                result = valid_foods[0]
                logging.info(f"Using first valid food: {result['description']}")

            if result:
                await cache.set_value(cache_key, result, time_to_live=3000)
                
                key = self._generate_cache_key(best_match_desc)
                await cache.set_value(key, result, time_to_live=3000)
                
            return result

        except Exception as e:
            logging.error(f"Error searching food.:{e}")
            return None