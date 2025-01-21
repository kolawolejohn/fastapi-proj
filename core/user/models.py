from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
import uuid
from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import UUID
from config import get_settings

settings = get_settings()


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    # posts = relationship("Post", back_populates="author")

    def hash_password(self, password: str):
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt).decode(
            "utf-8"
        )

    def verify_password(self, password):
        if not self.hashed_password:
            raise ValueError("Password is not hashed yet.")
        return bcrypt.checkpw(
            password.encode("utf-8"), self.hashed_password.encode("utf-8")
        )

    def generate_token(self):
        expiration = datetime.now(timezone.utc) + timedelta(hours=24)
        payload = {"sub": str(self.id), "exp": expiration}
        print("payload", payload)
        return jwt.encode(payload, f"{settings.SECRET_KEY}", algorithm="HS256")
