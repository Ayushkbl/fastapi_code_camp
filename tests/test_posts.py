import pytest

from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get('/posts/')
    print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get('/posts/')
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f'/posts/{test_posts[0].id}')
    assert res.status_code == 401

def test_get_one_post_not_exists(authorized_client, test_posts):
    res = authorized_client.get('/posts/8888')
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.Post(**res.json())
    assert post.id == test_posts[0].id
    assert post.content == test_posts[0].content
    assert post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("New trial title", "This is a new content", True),
    ("Donut", "Dunkin Donut Choco Chips Flavored", False),
    ("Titan", "The great watch company of India", None)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    payload = {
        "title": title,
        "content": content
    }
    if published != None:
        payload["published"] = published
    res = authorized_client.post("/posts/", json=payload)
    print(res.json())
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published if published != None else True
    assert created_post.user_id == test_user['id']
    

def test_unauthorized_user_create_post(client, test_user, test_posts):
    
    res = client.post(
        "/posts/", json={
            "title": "New Title",
            "content": "Unauthorized Entry",
            "published": True
        }
    )
    
    assert res.status_code == 401
    
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}"
    )
    
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}"
    )
    
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        "/posts/888"
    )
    
    assert res.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}"
    )
    print(f"Post 4 details: id:{test_posts[3].id}, title:{test_posts[3].title}, content:{test_posts[3].content}, user_id:{test_posts[3].user_id}")
    for post in test_posts:
        print(f"id:{post.id}, title:{post.title}, content:{post.content}, user_id:{post.user_id}")
    print(res.json())
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        'title': 'Updated Title',
        'content': 'Updated Content'
    }
    res = authorized_client.put(
        f'/posts/{test_posts[0].id}',
        json=data
    )
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_another_user_post(authorized_client, test_user, test_posts):
    data = {
        'title': 'Updated Title',
        'content': 'Updated Content'
    }
    res = authorized_client.put(
        f'/posts/{test_posts[3].id}',
        json=data
    )
    
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
            'title': 'Updated Title',
            'content': 'Updated Content'
        }
    res = client.put(
        f"/posts/{test_posts[0].id}",
        json=data
    )
    
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
            'title': 'Updated Title',
            'content': 'Updated Content'
        }
    res = authorized_client.put(
        "/posts/888",
        json=data
    )
    
    assert res.status_code == 404