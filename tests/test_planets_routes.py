def test_get_all_planets(client):
    # ACT
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_planet(client, one_saved_planet):
    # ACT
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "Earth",
        "radius": 6319,
        "description": "home planet"
    }

def test_get_one_planet_return_empty(client):
    # ACT
    response = client.get("/planets/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == []

def test_create_new_planet(client):
    # Act
    response = client.post("/planets", json={
        "name": "Jupiter",
        "description": "the largest planet in our solar system",
        "radius": 43441
    })

    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Jupiter",
        "description": "the largest planet in our solar system",
        "radius": 43441
    }
