def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/",
        json={'post_id': test_posts[3].id, "dir": 1}
    )
    assert res.status_code == 201

def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/",
        json={'post_id': test_posts[3].id, "dir": 1}
    )
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post(
        "/votes/",
        json={'post_id': test_posts[3].id, "dir": 0}
    )
    assert res.status_code == 201

def test_delete_vote_non_exists(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/",
        json={'post_id': test_posts[3].id, "dir": 0}
    )
    assert res.status_code == 404

def test_vote_post_non_exists(authorized_client, test_posts):
    res = authorized_client.post(
        "/votes/",
        json={'post_id': 9942, "dir": 1}
    )
    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    res = client.post(
        "/votes/",
        json={'post_id': test_posts[3].id, "dir": 1}
    )
    assert res.status_code == 401