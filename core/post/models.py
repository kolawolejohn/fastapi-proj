from datetime import datetime, timezone
import uuid
from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import UUID


class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String, index=True)
    content = Column(String)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
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
    author = relationship("User", backref="posts")
    # created_at = Column(
    #     TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    # )
    # updated_at = Column(
    #     TIMESTAMP(timezone=True),
    #     server_default=func.now(),
    #     onupdate=func.now(),
    #     nullable=False,
    # )
