from typing import List, Optional
from typing import Tuple

from fuzzywuzzy import fuzz


class FuzzyMatcherService:
    def __init__(self, threshold: int = 70): 
        self.threshold = threshold

    def get_top_matches(self, query: str, choices: List[str], top_n: int = 5) -> List[Tuple[str, int]]:
        if not query or not choices:
            return []

        query_lower = query.lower().strip()
        scores = []

        for choice in choices:
            choice_lower = choice.lower()
            
            ratio_score = fuzz.ratio(query_lower, choice_lower)
            partial_score = fuzz.partial_ratio(query_lower, choice_lower)
            token_sort_score = fuzz.token_sort_ratio(query_lower, choice_lower)
            token_set_score = fuzz.token_set_ratio(query_lower, choice_lower)
            
            composite_score = (
                ratio_score * 0.25 + 
                partial_score * 0.25 + 
                token_sort_score * 0.25 + 
                token_set_score * 0.25
            )
            
            if query_lower in choice_lower or choice_lower in query_lower:
                composite_score *= 1.2
            
            scores.append((choice, int(composite_score)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]

    def find_best_match(self, query: str, choice_options: List[str]) -> Optional[str]:
        if not query or not choice_options:
            return None

        query_lower = query.lower().strip()
        top_match = None
        best_score = 0

        for choice in choice_options:
            choice_lower = choice.lower()
            
            ratio_score = fuzz.ratio(query_lower, choice_lower)
            partial_score = fuzz.partial_ratio(query_lower, choice_lower)
            token_sort_score = fuzz.token_sort_ratio(query_lower, choice_lower)
            token_set_score = fuzz.token_set_ratio(query_lower, choice_lower)
            
            composite_score = (
                ratio_score * 0.25 + 
                partial_score * 0.25 + 
                token_sort_score * 0.25 + 
                token_set_score * 0.25
            )
            
            if query_lower in choice_lower or choice_lower in query_lower:
                composite_score *= 1.2
            
            composite_score = min(composite_score, 100)
            
            if composite_score > best_score and composite_score >= self.threshold:
                best_score = composite_score
                top_match = choice

        return top_match