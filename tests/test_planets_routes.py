def test_get_all_planets(client):
    # ACT
    response = client.get("/planets")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_one_planet(client, one_saved_planet):
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
