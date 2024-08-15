from time import time

from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware


class TimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        t0 = time()
        response: Response = await call_next(request)
        t1 = time()

        response.headers["X-Time"] = str(t1 - t0)
        return response
