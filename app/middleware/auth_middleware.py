from fastapi import Request
from jose import JWTError, jwt
from app.core.config import settings

async def auth_middleware(request: Request, call_next):
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer"):
        # token = auth_header.split(" ")[1]
        token = auth_header.split(maxsplit=1)[1] 

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            request.state.user = {
                "user_id": payload["user_id"],
                "role": payload["role"]
            }
        except JWTError:
            request.state.user = None
    else:
        request.state.user = None

    return await call_next(request)