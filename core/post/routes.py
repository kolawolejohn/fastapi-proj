from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .dependecy import get_post_for_user
from core.post.models import Post
from core.post.schema import CreateUpdatePost
from core.user.models import User
from dependencies import get_db, get_current_user

post_router = APIRouter()


@post_router.post("/posts")
def create_post(
    data: CreateUpdatePost,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    post = Post(title=data.title, content=data.content, author_id=user.id)
    db.add(post)
    db.commit()
    return {"data": data}


@post_router.get("/posts")
def list_posts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # posts = db.query(Post).all() this would fetch all including other users' post
    posts = db.query(Post).filter(Post.author_id == user.id).all()
    return {"data": [post.__dict__ for post in posts]}


@post_router.get("/posts/{id}")
def view_post(
    id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": post.__dict__}


@post_router.put("/post/{id}")
def edit_post(
    id: str,
    data: CreateUpdatePost,
    db: Session = Depends(get_db),
    post: Post = Depends(get_post_for_user),
):
    post.title = data.title
    post.content = data.content
    db.commit()
    return {"data": data}


@post_router.delete("/post/{id}")
def edit_post(
    id: str,
    db: Session = Depends(get_db),
    post: Post = Depends(get_post_for_user),
):
    db.delete(post)
    db.commit()
    return {"message": "Post Deleted Successfully"}
