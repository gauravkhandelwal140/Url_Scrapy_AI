from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
from starlette.responses import JSONResponse
from config.config import SECRET_API_KEY

# Custom Auth Middleware
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for open/public endpoints
        if request.url.path in ["/", "/open"]:
            return await call_next(request)
        # Get Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized: No token provided"})
        token = auth_header.split(" ")[1]
        
        if token != SECRET_API_KEY:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized: Invalid token"})
        # Auth passed, proceed
        return await call_next(request)