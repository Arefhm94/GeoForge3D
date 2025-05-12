from fastapi import Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .utils.security import verify_password
from .routers.auth import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")
    if token:
        try:
            payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
            request.state.user = await get_current_user(payload["sub"])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    response = await call_next(request)
    return response