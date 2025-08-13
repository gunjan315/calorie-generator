import time
from collections import defaultdict, deque
from config import get_settings
from fastapi import Request
from fastapi import HTTPException


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(deque)
        self.settings = get_settings()
        self.max_requests = self.settings.rate_limit_requests
        self.rate_limit_window_minutes = self.settings.rate_limit_window_minutes

    def is_req_allowed(self, ip: str) -> bool:
        curr_time = time.time()
                
        client_reqs = self.requests[ip]
        while client_reqs and client_reqs[0] < curr_time -(self.rate_limit_window_minutes* 60):
            client_reqs.popleft()
        
        if len(client_reqs) >= self.max_requests:
            return False
        
        client_reqs.append(curr_time)
        return True


rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    if not rate_limiter.is_req_allowed(request.client.host):
        raise HTTPException(
            status_code=429,
            detail="Rate limit reached! Plese try later"
        )
    
    response = await call_next(request)
    return response