from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db, get_settings, get_current_user
from core.user.models import User
from core.post.models import Post


def get_post_for_user(
    id, db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> Post:
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != user.id:
        raise HTTPException(
            status_code=401,
            detail="You do not have permission to get or modify this post",
        )
    return post
