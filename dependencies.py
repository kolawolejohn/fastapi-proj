from fastapi import Depends, HTTPException
import jwt
from core.user.models import User
from database import SessionLocal
from core.user.bearer import JWTBearer
from config import get_settings

settings = get_settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(JWTBearer())) -> User:
    try:
        payload = jwt.decode(token, f"{settings.SECRET_KEY}", algorithms=["HS256"])
        user_id = payload.get("sub")
        db = SessionLocal()
        result = db.query(User).filter(User.id == user_id).first()
        print("result", result)
        return db.query(User).filter(User.id == user_id).first()
    except (jwt.PyJWTError, AttributeError):
        raise HTTPException(status_code=401, detail="Invalid token")


# def get_current_user(token: str = Depends(JWTBearer())) -> User:
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         user_id = payload.get("sub")
#         if not user_id:
#             raise HTTPException(status_code=401, detail="Invalid token payload")

#         db = SessionLocal()
#         user = db.query(User).filter(User.id == user_id).first()
#         print(user)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
#     except jwt.PyJWTError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     except AttributeError:
#         raise HTTPException(status_code=500, detail="Unexpected server error")
