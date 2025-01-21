from datetime import datetime, time, timezone
from fastapi import HTTPException
import jwt
from config import get_settings

settings = get_settings()


def decodeJWT(token: str) -> dict:
    decoded_token = jwt.decode(token, f"{settings.SECRET_KEY}", algorithms=["HS256"])
    exp_timestamp = decoded_token.get("exp")
    if exp_timestamp:
        exp_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        current_time = datetime.now(timezone.utc)
        if exp_time >= current_time:
            return decoded_token
        else:
            print("Token is expired.")
            return None
    else:
        print("No expiration found in token.")
        return None


# def decodeJWT(token: str) -> dict:
#     decoded_token = jwt.decode(token, f"{settings.SECRET_KEY}", algorithms=["HS256"])
#     print("decoded_token", decoded_token)
#     return decoded_token if decoded_token["exp"] >= time.time() else None
