from fastapi.testclient import TestClient
from app import app
from tests.user.test_user_routes import get_user_data


client = TestClient(app)


def test_create_post():
    # Step 1: Log in to get an access token
    user_data = (
        get_user_data()
    )  # Replace with the actual function to fetch test user data
    login_response = client.post("/user/login", json=user_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # Step 2: Prepare the headers with the access token
    headers = {"Authorization": f"Bearer {access_token}"}

    # Step 3: Create post data
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content.",
    }

    # Step 4: Send a POST request to the create_post endpoint
    response = client.post("/posts", json=post_data, headers=headers)

    # Step 5: Assertions to validate the response
    assert response.status_code == 200
    assert response.json()["data"]["title"] == post_data["title"]
    assert response.json()["data"]["content"] == post_data["content"]

    # Additional validation if needed
    created_post = response.json()["data"]
    assert "id" not in created_post  # Assuming `id` is not included in the response


def test_list_posts():
    # Step 1: Create a test user and log them in
    user_data = get_user_data()  # Replace with your function for test user data
    login_response = client.post("/user/login", json=user_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Step 2: Create a test post for this user
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {"title": "User's Post", "content": "This post belongs to the user"}
    create_post_response = client.post("/posts", json=post_data, headers=headers)
    assert create_post_response.status_code == 200

    # Step 3: Create another post for a different user (simulate)
    another_user_data = get_user_data()  # Replace with another user's data
    another_login_response = client.post("/user/login", json=another_user_data)
    assert another_login_response.status_code == 200
    another_token = another_login_response.json()["access_token"]
    another_headers = {"Authorization": f"Bearer {another_token}"}
    another_post_data = {
        "title": "Another User's Post",
        "content": "This post belongs to another user",
    }
    another_post_response = client.post(
        "/posts", json=another_post_data, headers=another_headers
    )
    assert another_post_response.status_code == 200

    # Step 4: List posts for the original user
    list_posts_response = client.get("/posts", headers=headers)
    assert list_posts_response.status_code == 200
    posts = list_posts_response.json()["data"]

    # Step 5: Verify only the logged-in user's posts are fetched
    assert len(posts) == 1
    assert posts[0]["title"] == post_data["title"]
    assert posts[0]["content"] == post_data["content"]
