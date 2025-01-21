from core.post.models import Post
from core.user.models import User


def test_create_post():
    post = Post(title="My first post", content="This is me writing my first post")
    assert post.title == "My first post"
    assert post.content == "This is me writing my first post"


def test_user_post_relationship():
    user = User(username="user", email="user@user.com", hashed_password="password")
    post = Post(
        title="My first post", content="This is me writing my first post", author=user
    )
    assert post.author == user
    assert user.posts == [post]
