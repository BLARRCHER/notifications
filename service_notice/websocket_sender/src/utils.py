import jwt

from config import settings

JWT_ALGORITHM = "HS256"


def get_user_id(token: str) -> str | None:
    try:
        decoded_token = jwt.decode(token, settings.jwt_secret_key, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None

    return decoded_token["sub"]
