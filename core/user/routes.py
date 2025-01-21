from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .models import User
from .schema import UserCreate, UserLogin, Token
from dependencies import get_db

user_router = APIRouter()


@user_router.post("/signup")
def signup(data: UserCreate, db: Session = Depends(get_db)):
    user = User(username=data.username, email=data.email)
    user.hash_password(data.password)
    db.add(user)
    db.commit()
    return {"message": "User created Successfully"}


@user_router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if user is None or not user.verify_password(data.password):
        raise HTTPException(status_code=401, default="Invalid Credentials")
    token = user.generate_token()
    return Token(access_token=token, token_type="bearer")
